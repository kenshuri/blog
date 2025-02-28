---
title: Django + TailwindCSS + daisyUI
summary: Set-up a Django project with TailwindCSS and daisyUI
date: 2022-07-21
badge: code
image:
---

## Setting-up a django project working with TailwindCSS & daisyUI

In this tutorial, which is the first one published on this blog, we'll create a new django project from scratch and make it work with TailwindCSS and DaisyUI.

### Creating the django project
If you already have a django project and you're only interested in making it work with tailwindCSS and daisyUI, you should directly jump to the next part.

If you're reading this, it means that you are starting from scratch! Lucky you, nothing is more exciting than a blank page. As I'm writing this post while creating my blog, the example project for this tutorial will be a "Blog project". Let's get started!

#### 1. Creating the Django Project

Open a terminal (command, powershell...). Note that I might refer to a terminal as a shell in the rest of this tutorial. Then go to the folder of your choice where you want your future project to be, and run the following commands:
```shell
# shell

pip install virtualenv
python -m virtualenv venv
.\venv\Scripts\activate
pip install django 
django-admin startproject blogProject .
```

Bravo 👏 You just created a django project: that's also how [Neil Armstrong](https://fr.wikipedia.org/wiki/Neil_Armstrong) started 🚀! Before going any further, let's try to explain what each of this command did:

* `pip install virtualenv`: install the [virtualenv package](https://virtualenv.pypa.io/en/latest/index.html) on your computer. virtualenv is a tool to create isolated Python environments. It creates an environment that has its own installation directories, that doesn’t share libraries with other virtualenv environments (and optionally doesn’t access the globally installed libraries either).
* `python -m virtualenv venv`: actually creates the virtual environment that will be used in your project. It creates a directory `venv` that contains all libraries used in your project.
* `.\venv\Scripts\activate`: activate the virtual env! If you do not activate it and run the following command `pip install django`, it would install django as a library of your main python installation.
* `pip install django`: install the django library in your virtual environment. I suppose you did not expect you could create a django project without django right??
* `django-admin startproject blogProject .`: finally create the your django project using the django library you just installed! Here `blogProject` is the name of the project, you could change it to whatever please you.


If everything works correctly, you should be able to access your first *local*webpage served by your Django project. To do so, just run the following command in your shell:
```shell
# shell 

python manage.py runserver
```

In the terminal, you should see something like:
```
# shell output

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
July 19, 2022 - 21:42:23
Django version 4.0.6, using settings 'blogProject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Basically, django tells you that you successfully started your development server. If you now go to the address shown in the terminal `http://127.0.0.1:8000/`, you should see the default django landing page.

> I just remember that I created this blog to keep track of stuff that I do/like, not for it to actually be read by someone... Starting now, I'll get rid of stuff which won't be useful for a future myself 😄

#### Creating the blog App

```shell
#shell 

django-admin startapp blogApp
```


```python
# blogProject\settings.py

INSTALLED_APPS = [
    ...,
    'blogApp.apps.BlogappConfig',
    ...,
]

```

#### Creating the first view/page

```python
# blogApp\views.py

# Create your views here.
def index(request):
    return render(request, 'blogApp/index.html')
```


```python
# blogProject\urls.py

import blogApp.views

urlpatterns = [
    ...,
    path('', blogApp.views.index, name='index'),
    ...,
]
```


```html
<!--blogApp\templates\blogApp\base.html-->

{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <title>
        {% block title %}
        {% endblock title %}
    </title>
</head>
<body>
    <main>
        {%  block main %}
        {%  endblock main %}
    </main>
</body>
</html>
```


```html
<!--blogApp\templates\blogApp\index.html-->

{% extends "blogApp/base.html" %}

{% block title %}
    Landing Page
{% endblock title %}

{% block main %}
    <div>
    My landing page 🚀
    </div>
{% endblock main %}
```

Well done! At this stage, you should see a landing page saying **My landing page 🚀**

### Enabling tailwindCSS
To enable tailwindCSS, I followed the tuto on [this page](https://stackoverflow.com/questions/63392426/how-to-use-tailwindcss-with-django#63392427). We have to use the first method so that daisyUI can work too. Also, I agree with DD that using the django-tailwind packag seems a bit too magic!

In the terminal:
```shell
# shell

mkdir jstoolchains
cd jstoolchains
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

Configure your template paths in `tailwind.config.js` that have just been created, by specifying the right place to parse your content. This could be something like below or a little different, depending on where your templates are located:

```js
// jstoolchains/tailwind.config.js

content: ["../**/templates/**/*.html"],
```

In "upper folder", create an  `input.css`
```css
/* input.css*/

@tailwind base;
@tailwind components;
@tailwind utilities;
```

In your package.json file, prepare npm scripts to ease execution of tasks (adapt the paths according to your Django static folder location):


```json
// jstoolchains\package.json

"scripts": {
    "tailwind-watch": "tailwindcss -i ../input.css -o ../blogApp/static/css/output.css --watch",
    "tailwind-build": "tailwindcss -i ../input.css -o ../blogApp/static/css/output.css --minify"
  },
```

In the `<head>` tag of your `blogApp\templates\blogApp\base.html` file, add:
```html
<!--blogApp\templates\blogApp\base.html-->

<link rel="stylesheet" href="{% static "css/output.css" %}">
```

Tadaaaaa ✨✨ Tailwind is now configured in your django project!

To test it, run the follwing in a first terminal:
```shell
# shell

cd jstoolchains
npm run tailwind-watch
```

You should see that the police has changed 🤩

And in another terminal run:
```shell
# shell

python manage.py runserver
```

#### Auto-reload

At the moment, if you modify the source `html` file, even though the script `tailwind-watch` is running, you need to manually reload the browser to make the change appear. To have this happen automatically, you follow the tutorial on [this page](https://github.com/adamchainz/django-browser-reload)!

Run in the terminal:
```shell
# shell

python -m pip install django-browser-reload
```

Add django-browser-reload to your INSTALLED_APPS:

```python
# blogProject\settings.py

INSTALLED_APPS = [
    ...,
    'django_browser_reload',
    ...,
]
```

Include the app URL’s in your root URLconf(s):


```python
# blogProject\urls.py

from django.urls import include, path

urlpatterns = [
    ...,
    path('__reload__/', include('django_browser_reload.urls')),
]
```

Add the middleware:


```python
# blogProject\settings.py

MIDDLEWARE = [
    # ...
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    # ...
]
```

The middleware should be listed after any that encode the response, such as Django’s `GZipMiddleware`.

The middleware automatically inserts the required script tag on HTML responses before `</body>` when `DEBUG` is `True`. It does so to every HTML response, meaning it will be included on Django’s debug pages, admin pages, etc.

Félicitations !! We're almost done! 📯

### Enabling daisyUI

The last part is the easiest ;) Open a terminal, and run the following commands:
```shell
# shell

cd jstoolchains
npm install daisyui
```
Finally, modify your `jstoolchains\tailwind.config.js` file:
```js
// jstoolchains\tailwind.config.js

plugins: [require("daisyui")],
```

Et voilà!!

### Source code

The code with the set-up related to this project is available on [github](https://github.com/kenshuri/setup_django_tailwind_daisyui). Follow the README instructions to set-up your Django project working with TailwindCSS and daisyUI out of the box.


### Sources

* [https://justdjango.com/blog/build-a-blog-with-django#create-apps]()
* [https://stackoverflow.com/questions/63392426/how-to-use-tailwindcss-with-django#63392427]()
* [https://github.com/adamchainz/django-browser-reload]()
