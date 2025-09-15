from __future__ import annotations

import os
import io
import glob
import urllib.request
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

try:
    import pandas as pd
except ImportError as e:
    raise CommandError("Cette commande nécessite pandas: pip install pandas") from e

try:
    from PIL import Image
except ImportError as e:
    raise CommandError("Cette commande nécessite Pillow: pip install pillow") from e


def _ensure_rgb(img: Image.Image) -> Image.Image:
    # Convertit en RGB pour éviter les soucis (P/LA/RGBA...)
    if img.mode not in ("RGB", "L"):
        return img.convert("RGB")
    return img


class Command(BaseCommand):
    help = "Télécharge les couvertures OpenLibrary à partir d'un export Goodreads et les optimise pour le web."

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=str, default="goodreads_library_export.csv")
        parser.add_argument("--since", type=str, default="2020-01-01")
        parser.add_argument(
            "--out-dir",
            type=str,
            default=str(Path(settings.BASE_DIR) / "core" / "static" / "images" / "covers"),
        )
        parser.add_argument("--min-size", type=int, default=1000)
        parser.add_argument("--limit", type=int, default=None)
        parser.add_argument("--overwrite", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

        # Nouveaux paramètres d'optimisation
        parser.add_argument(
            "--format",
            choices=["webp", "avif", "jpeg"],
            default="webp",
            help="Format de sortie optimisé (défaut: webp).",
        )
        parser.add_argument(
            "--quality",
            type=int,
            default=80,
            help="Qualité d'encodage (0-100) – défaut: 80.",
        )
        parser.add_argument(
            "--max-width",
            type=int,
            default=1200,
            help="Largeur max de l'image (redimensionnement conservant le ratio). Défaut: 1200 px.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv"])
        if not csv_path.is_absolute():
            csv_path = Path(settings.BASE_DIR) / csv_path

        since_str = options["since"]
        out_dir = Path(options["out_dir"])
        min_size = options["min_size"]
        limit = options["limit"]
        overwrite = options["overwrite"]
        dry_run = options["dry_run"]

        out_format = options["format"].lower()
        quality = int(options["quality"])
        max_width = int(options["max_width"])

        # Validations & setup
        try:
            since = datetime.strptime(since_str, "%Y-%m-%d").date()
        except ValueError:
            raise CommandError("--since doit être au format YYYY-MM-DD")

        if not csv_path.exists():
            raise CommandError(f"CSV introuvable: {csv_path}")

        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)

        self.stdout.write(self.style.NOTICE(f"Lecture du CSV: {csv_path}"))
        books_data = pd.read_csv(csv_path)
        books_data = books_data.rename(columns=str.lower).rename(
            columns={"my rating": "my_rating", "average rating": "gr_rating"}
        )

        if "date read" not in books_data.columns:
            raise CommandError("Colonne 'Date Read' absente du CSV Goodreads.")

        books_data["date_read"] = pd.to_datetime(
            books_data["date read"], format="%Y/%m/%d", errors="coerce"
        ).dt.date
        books_data = books_data[books_data["date_read"].notna()]
        books_data = books_data[books_data["date_read"] >= since]

        if "isbn" not in books_data.columns:
            raise CommandError("Colonne 'ISBN' absente du CSV Goodreads.")
        books_data["isbn"] = (
            books_data["isbn"]
            .astype(str)
            .str.replace("=", "", regex=False)
            .str.replace('"', "", regex=False)
        )

        keep_cols = ["title", "author", "date_read", "my_rating", "gr_rating", "isbn"]
        missing = [c for c in keep_cols if c not in books_data.columns]
        if missing:
            raise CommandError(f"Colonnes manquantes dans le CSV: {missing}")

        books_data = (
            books_data[keep_cols]
            .sort_values("date_read", ascending=False)
            .reset_index(drop=True)
        )

        if limit:
            books_data = books_data.head(limit)

        total = len(books_data)
        self.stdout.write(self.style.NOTICE(f"{total} livres à traiter (depuis {since})."))
        if dry_run:
            self.stdout.write(self.style.WARNING("Mode --dry-run activé : aucun fichier ne sera écrit."))

        # Boucle principale
        processed = 0
        for _, row in books_data.iterrows():
            isbn = (row.get("isbn") or "").strip()
            if not isbn or isbn.lower() in ("nan", "none"):
                continue

            src_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
            suffix = {"webp": "webp", "avif": "avif", "jpeg": "jpg"}[out_format]
            out_file = out_dir / f"{isbn}-cover.{suffix}"

            if out_file.exists() and not overwrite:
                continue

            if dry_run:
                self.stdout.write(f"[DRY] Télécharger & optimiser {src_url} -> {out_file}")
                processed += 1
                continue

            try:
                # Téléchargement en mémoire
                with urllib.request.urlopen(src_url, timeout=20) as resp:
                    raw = resp.read()

                # Ignore les “faux” jpg minuscules avant même d’ouvrir Pillow
                if len(raw) < min_size:
                    continue

                # Ouverture & conversion
                with Image.open(io.BytesIO(raw)) as img:
                    img = _ensure_rgb(img)

                    # Redimensionnement doux si nécessaire
                    if max_width and img.width > max_width:
                        new_height = int(img.height * (max_width / img.width))
                        img = img.resize((max_width, new_height), Image.LANCZOS)

                    # Sauvegarde optimisée (métadonnées non conservées)
                    save_kwargs = {}
                    if out_format == "webp":
                        # method=6 = meilleur effort, optimize=True, quality param
                        save_kwargs = {"quality": quality, "method": 6}
                        img.save(out_file, format="WEBP", **save_kwargs)
                    elif out_format == "avif":
                        # AVIF nécessite pillow-avif-plugin (pip install pillow-avif-plugin)
                        # quality≈0-100 (selon plugin), effort=9 ≈ compression + lente
                        save_kwargs = {"quality": quality}
                        try:
                            img.save(out_file, format="AVIF", **save_kwargs)
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"AVIF indisponible ({e}). Bascule en WEBP pour {isbn}."
                                )
                            )
                            img.save(out_file, format="WEBP", quality=quality, method=6)
                    else:  # jpeg
                        save_kwargs = {"quality": quality, "optimize": True, "progressive": True}
                        img.save(out_file, format="JPEG", **save_kwargs)

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"{e} pour l'ISBN {isbn}"))
                continue

            processed += 1
            if processed % 20 == 0:
                self.stdout.write(f"Progression: {processed}/{total}")

        # Nettoyage d’anciennes “vides” restant en .jpg (si tu en gardes encore)
        deleted = 0
        for ext in ("*.jpg", "*.jpeg", "*.webp", "*.avif"):
            for c in glob.glob(str(out_dir / ext)):
                try:
                    if os.stat(c).st_size < min_size:
                        if dry_run:
                            self.stdout.write(f"[DRY] Supprimer (trop petit) : {c}")
                        else:
                            os.remove(c)
                        deleted += 1
                except FileNotFoundError:
                    continue

        self.stdout.write(
            self.style.SUCCESS(
                f"Terminé. Optimisées: ~{processed}, supprimées (trop petites): {deleted}"
            )
        )
