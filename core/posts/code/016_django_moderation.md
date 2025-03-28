---
title: Add a Moderation app to a Django application
summary: Migrate domain from O2Switch to Clouflare
date: 2050-04-02
badge: code
image:
---

### 🚦 **Modération automatique des annonces avec Mistral AI**  

**Problème actuel :**  
- Il n’y a pas de modération automatique des annonces, ce qui peut entraîner la publication de contenus inappropriés ou hors sujet.  
- La modération manuelle est coûteuse en temps et en effort.  

**Solution proposée :**  
1. **Tester la modération avec l’API de Mistral AI** :  
   - Exécuter une analyse sur toutes les annonces déjà publiées pour voir lesquelles seraient rejetées par l’API.  
   - Vérifier si l’API fournit des raisons détaillées pour les exclusions.  
   - Évaluer le coût et la pertinence du service avant de l’intégrer en production.  

2. **Intégration de la modération automatique lors de la soumission d’une annonce** :  
   - Lorsqu’un utilisateur soumet une annonce, elle est automatiquement analysée par l’API de Mistral AI.  
   - Si l’annonce est jugée inappropriée, un message d’erreur est affiché à l’utilisateur avec les raisons précises.  
   - L’utilisateur peut modifier son annonce et la resoumettre immédiatement.  

3. **Améliorer l’expérience utilisateur** :  
   - Afficher un message clair en cas de rejet pour guider l’utilisateur sur les modifications nécessaires.  
   - Ajouter une option pour demander une réévaluation manuelle si l’utilisateur pense que son annonce a été injustement bloquée.  

**Objectif final :**  
- Vérifier l’efficacité et le coût de l’API avant d’adopter définitivement la solution.  
- Améliorer la qualité des annonces publiées sans alourdir le processus de soumission.


### Étape 1 : Tester la modération avec l’API de Mistral AI  

Nous allons procéder méthodiquement pour tester la solution avant de l’intégrer en production.

---

#### 🔍 **1.1 Collecte des annonces existantes**  
Avant de tester l’API, nous avons besoin d’un ensemble représentatif d’annonces déjà publiées. Voici comment procéder :
- Exporter un échantillon d’annonces publiées (exemple : les 1 000 dernières).
- S’assurer que ces annonces couvrent différents types de contenus (textes acceptables, potentiellement problématiques, hors sujet, etc.).
- Si possible, inclure des annonces ayant déjà été signalées ou modérées manuellement.

👉 **Action** : Extraire les annonces depuis la base de données ou l’interface d’administration.

---

#### ⚙️ **1.2 Envoyer les annonces à l’API de Mistral AI**  
Une fois les annonces collectées, nous allons les envoyer à l’API pour voir comment elle les analyse.  
Points à vérifier :
- **Méthode d’appel** : Quelle requête HTTP faut-il utiliser (POST, GET) ?  
- **Format des données** : JSON, texte brut, ou autre ?  
- **Réponse de l’API** : Quels types de feedback fournit-elle (score, catégorie, raison du rejet) ?

👉 **Action** :  
- Se référer à la documentation de l’API de Mistral AI pour connaître les paramètres et le format requis.  
- Préparer un script de test en Python (ou un autre langage utilisé dans votre projet).  

---

#### 📊 **1.3 Analyser les résultats**  
Une fois les annonces analysées, nous devons évaluer la pertinence des résultats :
- **Taux de rejet** : Combien d’annonces sont marquées comme inappropriées ?  
- **Justification fournie** : L’API donne-t-elle des raisons claires pour chaque rejet ?  
- **Précision de l’analyse** : Comparez avec des modérations manuelles pour voir si l’API est fiable.

👉 **Action** :  
- Stocker les résultats dans un tableau comparatif (annonce + verdict de l’API).  
- Vérifier s’il y a des erreurs évidentes (faux positifs ou faux négatifs).  

---

#### 💰 **1.4 Évaluation du coût et de la pertinence**  
Enfin, nous devons déterminer si cette solution est viable à long terme :
- **Coût par requête** : Combien coûte une analyse d’annonce ?  
- **Coût total estimé** : En fonction du volume d’annonces soumises quotidiennement.  
- **Pertinence** : L’API apporte-t-elle une réelle valeur ajoutée par rapport à une modération humaine ?  

👉 **Action** :  
- Calculer le coût total pour un mois de fonctionnement.  
- Comparer avec le temps économisé sur la modération humaine.  

---

### 🎯 **Livrables attendus à la fin de cette étape**  
✅ Un rapport avec :
- Une analyse du taux de rejet et des justifications fournies par l’API.  
- Un tableau comparatif avec les annonces et les résultats de l’API.  
- Une estimation des coûts et des bénéfices.  

Si les résultats sont satisfaisants, nous pourrons alors passer à l’étape suivante : l’intégration en production. 🚀