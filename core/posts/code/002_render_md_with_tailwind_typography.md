---
title: Django + Markdown
summary: Render markdown document in Django
date: 2022-07-22
badge: code
image:
---

## Render Markdown documents in django template with TailwindCSS typography

### Install tailwindcss typography

```shell
cd jstoolchains
npm install -D @tailwindcss/typography
```

Then add the plugin to your `tailwind.config.js` file:
```js
module.exports = {
  //...
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}
```

You can test that the installation was succesfful by adding the class `prose` in your `index.html`.
```html
{% block main %}
    <article class="prose">
        <h1>H1 title</h1>
        <p>Some text</p>
        <h2>H2 title</h2>
    </article>
{% endblock main %}
```

### Install django-mardownify

The [installation instructions](https://django-markdownify.readthedocs.io/en/latest/install_and_usage.html) are summarized below.

In your terminal run:
```shell
pip install django-markdownify
```

and add markdownify to your installed apps in `settings.py`:
```python
INSTALLED_APPS = [
    # ...,
    'markdownify.apps.MarkdownifyConfig',
]
```

You can now test that the installation was successful.

Load the tag in your template `index.html` and add some markdown:

```html
{% load markdownify %}
<!--...-->
<p>{{ '[Index]()'|markdownify }}</p>
```

This `'[Index]()'` should be transform as link thanks to the markdownify tag.

### Render a full md file in your template

Let's first create a simple file `md_file.md` that will act as an example. This example file was taken from [https://www.makeareadme.com/](). Save this file under `blogApp\posts\md_file.md`.

````md
[//]: # (blogApp/posts/md_file.md)

# Foobar

Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
````

Now, you need to modify your view so that your `md_file` is given to your template in the `context` variable.

```python
import os

# Create your views here.
def index(request):
    md_file = open(os.path.join(os.path.dirname(__file__), 'posts/md_file.md'), encoding="utf-8").read()
    context = {
        'md_file': md_file
    }
    return render(request, 'blogApp/index.html', context)
```

Finally, modify your template `index.html`
```html
{% block main %}
    <article class="prose">
        {{ md_file|markdownify }}
    </article>
{% endblock main %}
```

At this stage, you should see something like this:
![](C:\Users\alexi\PycharmProjects\blogProject\blogApp\static\blogApp\002_01_md_file_tentative.jpg)

It is not exactly what we wanted. The reason for this is that the markdownify package *[bleach](https://django-markdownify.readthedocs.io/en/latest/settings.html#disable-sanitation-bleach)ed* the md output. To get the desired result, we need to modify `settings.py`

```python
# settings.py

# Markdownify settings
MARKDOWNIFY = {
    "default": {
        "BLEACH": False,
    }
}
```

Well done! It's already better. However, the code block does not work yet... Again, we can modify the settings of the Markdownify tag to suit our needs and [enable the necessary extensions](https://django-markdownify.readthedocs.io/en/latest/settings.html#enable-markdown-extensions)! 
```python
# settings.py

# Markdownify settings
MARKDOWNIFY = {
    "default": {
        "MARKDOWN_EXTENSIONS": [
            'markdown.extensions.extra',
        ],
        "BLEACH": False,
    }
}
```

Looking good! May we have some code highlighting maybe?

To do that, first we need to add the `codehilite` extension in `seetings.py`

```python
# settings.py

# Markdownify settings
MARKDOWNIFY = {
    "default": {
        "MARKDOWN_EXTENSIONS": [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ],
        "BLEACH": False,
    }
}
```

Then, we need to follow the steps descibed [here](https://python-markdown.github.io/extensions/code_hilite/) so that the `codehilite` extension works properly (thanks unknown friend for [this post](https://github.com/erwinmatijsen/django-markdownify/issues/32#issuecomment-1120137357)). So run the following commands:

```shell
pip install Pygments
pygmentize -S github-dark -f html -a .codehilite > codehilite.css
```

> Please note that `Pygments` is fully needed for it to work. It is not only used to create the `css` file.

Then move the newly created `codehilite.css` file in your `static\css` folder, and reference this new css file in your `base.html` template!
```html
<!--base.html-->
<link rel="stylesheet" href="{% static 'css/codehilite.css' %}">
```

Well done, it should now be working fine!

I faced an error where the `css` file generated was not in utf-8 format, leading to a failure when running collecstatic.
On windows, the previous command can be amended to:

```shell
pygmentize -S github-dark -f html -a .codehilite | Out-File -FilePath codehilite.css -Encoding utf8
```

## Source code
The source code relative to this project is available [here](https://github.com/kenshuri/render_md_with_tailwind_typography).

## Sources
Material used for this tutorial

* [https://daisyui.com/docs/layout-and-typography/]()
* [https://github.com/tailwindlabs/tailwindcss-typography/blob/master/README.md]()
* [https://github.com/kenshuri/setup_django_tailwind_daisyui]()
* [https://learndjango.com/tutorials/django-markdown-tutorial]()
* [https://stackoverflow.com/questions/61666570/render-markdown-to-html-in-django-templates]()
* [https://github.com/erwinmatijsen/django-markdownify]()
* [https://django-markdownify.readthedocs.io/en/latest/index.html]()
* [https://python-markdown.github.io/]()
* [https://python-markdown.github.io/extensions/code_hilite/]()

