---
title: Django + TailwindCSS + daisyUI deploy to Heroku
summary: Deploy your Django + TailwindCSS + daisyUI app to Heroku
date: 2022-08-25
badge: code
image:
---

## Deploy a Django + Tailwind + daisyUI application to Heroku

To use as an example, we will start from a new project already setup with Django + Tailwind + daisyUI available on [github](https://github.com/kenshuri/setup_django_tailwind_daisyui).

```shell
git clone https://github.com/kenshuri/setup_django_tailwind_daisyui.git 005_deploy_to_heroku
cd 005_deploy_to_heroku
```

### Deploy to Heroku

#### [Create a Heroku Remote](https://devcenter.heroku.com/articles/git#create-a-heroku-remote)

```shell
heroku create -a deploy-to-heroku-blog-example
git remote -v
```

#### [Deploy the code](https://devcenter.heroku.com/articles/git#deploy-your-code)

```shell
git push heroku main
```

But it won't be so easy! You should see the below error message:
```
remote:  !     Error while running '$ python manage.py collectstatic --noinput'.
remote:        See traceback above for details.
remote:
remote:        You may need to update application code to resolve this error.
remote:        Or, you can disable collectstatic for this application:
remote:
remote:           $ heroku config:set DISABLE_COLLECTSTATIC=1
remote:
remote:        https://devcenter.heroku.com/articles/django-assets
remote:  !     Push rejected, failed to compile Python app.
remote: 
remote:  !     Push failed
remote: Verifying deploy...
remote:
remote: !       Push rejected to deploy-to-heroku-blog-example.
remote:
To https://git.heroku.com/deploy-to-heroku-blog-example.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to 'https://git.heroku.com/deploy-to-heroku-blog-example.git'
```

It's very normal as Django does not support serving static files in production. A solution is proposed below:

#### [Django and static assets in production](https://devcenter.heroku.com/articles/django-assets)

Follow instructions available on that [page](https://whitenoise.evans.io/en/stable/django.html). To sum-up, you'll need to:

- Install whitenoise
```shell
pip install whitenoise
```

- Add the following to your `settings.py`
```python
# settings.py

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / "staticfiles"
```

- Edit your `settings.py` file and add WhiteNoise to the MIDDLEWARE list. The WhiteNoise middleware should be placed directly after the Django SecurityMiddleware (if you are using it) and before all other middleware:
```python
# settings.py

MIDDLEWARE = [
    # ...
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]
```

Now, you could commit and try again to deploy your app to Heroku...

```shell
git push heroku main
```

The deployment is successful!! Now go and check your app... What the heck??!! Something is wrong and you should see an error message saying:
>#### Application error
>
>An error occurred in the application and your page could not be served. If you are the application owner, check your logs for details. You can do this from the Heroku CLI with the command
>
>`heroku logs --tail`

Again, this was to be expected, we're not done yet! At the moment, as indicated by the error message, there is **no web process running**.

#### Add a `Procfile` and setup `gunicorn`

As described [here](https://devcenter.heroku.com/articles/django-app-configuration), Heroku web applications require a `Procfile`. This file is used to explicitly declare your application’s process types and entry points. It is located in the root of your repository.

The `Procfile` uses `gunicorn`, we thus need to install it following the instructions available on [this page](https://devcenter.heroku.com/articles/django-app-configuration). As a summary:

- Install gunicorn
```shell
pip install gunicorn
```

- Add a `Procfile` to project root containing simply the following. The name of the app (before `.wsgi below`) is from the value of the `WSGI_APPLICATION` variable define in your `settings.py`.
```text
Procfile

web: gunicorn blogProject.wsgi
```

- Update your requirements.txt to add `gunicorn`
```shell
pip freeze > requirements.txt
```

- Commit and push to heroku


We're not there yet ! You should see an error message complaining about **DisallowedHost at /** 

#### Add ALLOWED_HOSTS

You need to specify in your `settings.py` that your application should accept connection coming from your application domain... To do so, modify the variable ALLOWED_HOSTS defined in your `settings.py`. In my case, in need to do:

```python
# settings.py

ALLOWED_HOSTS = ['deploy-to-heroku-blog-example.herokuapp.com']
```

Commit again, and push to heroku!

> Bravoooooo!!!!

You should see the landing page :) But wait, something is not right... 

...

...

...

The design is wrong!! Tailwind and daisyUI are not used!!!! This is the worst tutorial ever :'( 

No worries, we're almost there! We just need to add the css file to our git repo! Run the following commands:

```shell
cd jstoolchains
npm run tailwind-build
```

This will automatically creates a minified css file in your app `static` folder. Finally, commit and push to heroku...

> Finally!! It should be all good now ;)

### (Optionnal - Security Warnings) DEBUG mode and SECRET_KEY

In your `setttings.py` file, two settings should get your attention, see below:

```python
# settings.py

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-blablabla'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'True'
```

Well, actually, the `SECURITY WARNING` comment in CAPITAL letters should! These are the **critical settings listed in [django deployment checklist](https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/#critical-settings)** Let's take care of these warnings 💪

#### DEBUG mode

The DEBUG mode is enable by default though the seeing `DEBUG` when you start a new django project. 
As its name  suggests, it is useful when you are debuging as it shows useful information when a bug occurs. 
However, you do not want to have this mode actovated in Production as it could give unsafe information to 
someone with bad intentions 👿

Let's code a logic so that it is enabled by default when you are working locally and disabled otherwise. 
To do so, we will rely on the package [`python-dotenv`](https://pypi.org/project/python-dotenv/). Let's install it:

```shell
pip install python-dotenv
```

Then, create a `.env` file at your project root containing the following:

```text
.env <- That's just the name of the file repeated here

DJANGO_DEBUG=True
```

Finnaly, modify your `settings.py` file so that the `.env` file settings are read.

```python
# settings.py

import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = os.environ.get("DJANGO_DEBUG") == 'True'
```

Thanks to this piece of code, the `DEBUG` variable is `True` if `DJANGO_DEBUG` is `True`, `False` otherwise. 
You can know deploy your modified app to Heroku!

If you now try to acces a non-existing page on your website, you see an error page with addtional information because 
the DEBUG is activated: indeed, your app load the DJANGO_DEBUG config in your `.env` file.

By default, `load_dotenv` doesn't override existing environment variables, so to make sure that the DEBUG mode 
is disabled in PRODUCTION, you'll need to add the `DJANGO_DEBUG = False` to your app environment on Heroku.
You can do so by going in you App settings, then Config Vars 🙂. 
If you try again to acces a non-existing page on your website, you should see a regular error message!

#### SECRET_KEY

As suggested in the comment in your `settings.py`, the secret key used in production should be kept secret!
Building on the same `.env` used before, we will create 2 separate SECRET_KEY

- 1 used in production, saved as a Config Var in your app settings on Heroku
- 1 used for development, saved in your .env file

To create secret keys, the easiest is to use the django built-in function [`get_random_secret_key`](https://github.com/django/django/blob/3c447b108ac70757001171f7a4791f493880bf5b/django/core/management/utils.py#L82)

```python
# Python console

from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

Then in your `settings.py` change the secret key value so that it uses environment variable.

```python
# settings.py

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
```

Bravo!! You can now safely deploy your app to Heroku! 👏

### Source code

The final version of this tutorial code is available on [github](https://github.com/kenshuri/django_tailwind_heroku)!