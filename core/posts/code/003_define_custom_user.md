---
title: Django Custom User Model
summary: Define a Custom User Model in Django
date: 2022-07-25
badge: code
image:
---

## Define a custom user model for your django project

In this tuto, we will add a custom user model to use an email as username. You can get started by using the django project below, which is set-up to work out-of-the-box with tailwindCSS and daisyUI (see here my other [post](https://kenshuri-blog.herokuapp.com/posts/001_setup_django_tailwind_daisyui.md) for details)

```shell
git clone https://github.com/kenshuri/setup_django_tailwind_daisyui.git .\003_define_custom_user\
cd .\003_define_custom_user\
```

### Create a new app to deal with accounts

If you want to check for disposable email domains, install [`django-email-blacklist`](https://github.com/Zeioth/django-email-blacklist).  You will then be able to check if a new user is using disposable email when writing your sign-up form.

```shell
pip install django-email-blacklist
```

Get the accounts app from [github](https://github.com/kenshuri/django_tailwind_daisyui_customusermodel) and save the folder `accounts` at your project root. 

### Integrate in main project

```python
# setting.py

# Application definition
INSTALLED_APPS = [
    # ...
    'accounts',
    # ...
]

# Custom User model
AUTH_USER_MODEL = 'accounts.CustomUser'

DISPOSABLE_EMAIL_DOMAINS = "accounts/blacklist/disposable_email_domains.txt"
```

### Set-up project

```shell
python manage.py makemigrations
```

You should see the following output:
```
Migrations for 'accounts':
  accounts\migrations\0001_initial.py
    - Create model CustomUser
```
If not, the main chance is that you forgot to add `accounts` to the list of installed apps in `settings.py`. **Do not run the migrations while the migrations on accounts app in not ready!**

Then, **if the migration is ready, ie you saw the above message after running `makemigrations`**, run the following commands:
```shell
python manage.py migrate
python manage.py createsuperuser
```

You can see that an **Email address** is asked instead of a username. Et voilà! You're good to go :)

### Finish set-up if you started from the proposed project
```shell
cd jstoolchains
npm install
npm run tailwind-watch
```

```shell
python manage.py runserver
```