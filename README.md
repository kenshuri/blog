# blog

## DEV

### Updates

#### Books

- Go to: https://www.goodreads.com/review/import
- Save library as `goodreads_library_export.csv` 
- Run `python manage.py get_covers`


#### DaisyUI

```shell
npm i -D daisyui@latest
```

### Aliases

#### Useful Aliases

- `uvm`: `uv run manage.py`
- `uvmr`: `uv run manage.py runserver`
- `twb` : `npm run tailwind-build`
- `dev` : Start tailwind-watch and runserver

#### Profile

```Profile
Remove-Item Alias:curl -Force
Function uvm {
    python manage.py $args
}
Function uvmr {
    python manage.py runserver
}
Function twb {
    cd jstoolchains
    npm run tailwind-build
    cd ..
}
function dev {
    cd jstoolchains
    Start-Job -ScriptBlock { npm run tailwind-watch }
    cd ..
    python manage.py runserver
}
```

#### Add new Aliases

Add new Aliases by creating function: 
```shell
notepad $PROFILE
```

### Code color in Markdown

The style for the coloring of the code is based on Pygments, see my blog post about it. To change color, you can 
geenrate a new codehilite.css file as below:

```shell
pygmentize -S github-dark -f html -a .codehilite > codehilite.css
```

You can change the theme `github-dark` for other themes. The list of styles is obtained with `pygmentize -L style`.

To make sure the `css` file is genarated in utf-8 (if not, the collectstatic command will fail), on windows you can amend the previous command to:

```shell
pygmentize -S github-dark -f html -a .codehilite | Out-File -FilePath codehilite.css -Encoding utf8
```

