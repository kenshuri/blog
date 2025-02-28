---
title: Move your Django App from Heroku to CapRover
summary: With free Heroku hosting stopping on November 28th, 2022, it's time to move!
date: 2022-10-23
badge: code
image:
---

# Move your Django App from Heroku to CapRover

## Why should you move?

I guess that if you're here, you already know... Quite sadly, starting November 28th, 2022, free Heroku Dynos and free Heroku Postgres will no longer be available.
While many devs happily used Heroku for their hobby projects and spend almost no time worrying about deployment, 
now is a good time to find another option than Heroku.

There are several good options out there, but today we'll be talking about [CapRover](https://caprover.com/). 
I chose [CapRover](https://caprover.com/) after a quick *literature review*, see for instance [here](https://dev.to/lorenzojkrl/bye-bye-heroku-2npi), [there](https://dev.to/timhub/self-host-heroku-alternative-40l4) or [there](https://github.com/ripienaar/free-for-dev#web-hosting).

CapRover describes itself as 
>*an extremely easy to use app/database deployment & web server manager for your NodeJS, Python, PHP, ASP.NET, Ruby, MySQL, MongoDB, Postgres, WordPress (and etc...) applications! It's blazingly fast and very robust as it uses Docker, nginx, LetsEncrypt and NetData under the hood behind its simple-to-use interface.*

Before going further, please note that I could not find a 100% free replacement for Heroku. CapRover is free and will remove from your 
shoulders most of the complexity of deploying your apps, but to make it work you still need:
- a VPS server of your choice: around 5$/month
- a domain name: around 10$/year

Good luck to find 100% free providers for these 😉 Now that this is clear, let's [get started](https://caprover.com/docs/get-started.html)!

**Summary**
1. Get yourself a domain name
2. Get yourself a server
3. Set-up DNS
4. Deploy your app to CapRover
5. Deploy a Django app with heavier dependencies
6. Go full DevOps

If you want to go straight to the code, see [here](https://github.com/kenshuri/django_tailwind_caprover).

## 1. Get yourself a domain name 

I won't list all the existing options as many have done it already... You can look [here](https://themeisle.com/blog/best-domain-registrars/), or [here](https://www.codeinwp.com/blog/cheap-domains/) for instance. 
In my case I chose [OVHCloud](https://www.ovhcloud.com/en-ie/domains/) as it competed well with others in terms of pricing and has its headquarters in my country.

## 2. Get yourself a server

Choosing a server is more delicate than choosing a domain name. To do so, you should follow the [requiremnts listed
by CapRover](https://caprover.com/docs/get-started.html#b2-server-specs).

In my case, I chose the easy way, the one recommended by CapRover, which is 
>*to install CapRover is via DigitalOcean one-click app. CapRover is available as a One-Click app in DigitalOcean marketplace.*

So I simply used [this link](https://marketplace.digitalocean.com/apps/caprover?action=deploy&refcode=6410aa23d3f3) to create a droplet (ie a server in DigitcalOcean vocabulary)

## 3. Set-up DNS

Now, you need to *connect* your domain to your server. 
To do so, you need to change the DNS settings, so that when you connect to your domain, you're being redirected to your server.
You need to create an `A-record` in your DNS settings. It should be quite straight-forward to do in your domain manager website.

In my case, I need to go to [OVH manager](https://www.ovh.com/manager/#/web/configuration) and then

1. Click on [Domain names]()
2. Select my [domain name](). 
3. Click on [DNS zone]()
4. And finally [Add an entry]()

[![saf17s.md.jpg](https://iili.io/saf17s.md.jpg)](https://freeimage.host/i/saf17s)

Then, create an `A-record` and 

1. Choose any sub-domain: in my case I chose `blog`
2. As a target, use the ipv4 address of your server (or droplet if you're using DigitalOcean) 

[![saCrQ4.md.jpg](https://iili.io/saCrQ4.md.jpg)](https://freeimage.host/i/saCrQ4)

## Set-up CapRover on your server

*from [CapRover Getting started doc](https://caprover.com/docs/get-started.html#step-3-install-caprover-cli)*

Assuming you have npm installed on your local machine (e.g., your laptop), simply run (add sudo if needed):

```shell
npm install -g caprover
```

Then, run
```shell
caprover serversetup
```

Below are the several steps and the answer to give if you are hesitating.

```shell
PS C:\Users\alexi> caprover serversetup

Setup CapRover machine on your server...

? have you already started CapRover container on your server? Yes
? IP address of your server: Your server (droplet) ipv4 address 
? CapRover server root domain: blog.yourdomain.com assuming that you set *.blog.mydomain.com to point to your IP address when creating the A-record
? new CapRover password (min 8 characters): [hidden]
? enter new CapRover password again: [hidden]
? "valid" email address to get certificate and enable HTTPS: your.mail@mail.com
? CapRover machine name, with whom the login credentials are stored locally: captain-01

CapRover server setup completed: it is available as captain-01 at https://captain.blog.yourdomain.com

For more details and docs see CapRover.com
```
As prompted, you can now visit the page `https://captain.blog.yourdomain.com`.

## 4. Deploy your app to CapRover

To deploy to CapRover, you will need a [**Captain Definition File**](https://caprover.com/docs/captain-definition-file.html).
This file plays a similar role to the `Procfile` when you're deploying to Heroku. 
It describes the foundation to run your app: its language and version.
As the `Procfile`, it needs to sit at the root of the project, next to the `requirements.txt` file.

In our case, as we are deploying a django app, it should contain the following (depending on your python version).

```text
 {
  "schemaVersion": 2,
  "templateId": "python-django/3.10"
 }
```

In order to try and actually deploy something, you could clone [this project](https://github.com/kenshuri/django_tailwind_caprover) and
follow the instructions in the `README`.

### 4.1. Create a CapRover app

On the page `https://captain.blog.yourdomain.com`, in `Apps`, create a new app with the name of your choice.

[![saVdve.md.jpg](https://iili.io/saVdve.md.jpg)](https://freeimage.host/i/saVdve)

Then, go in your config in CapRover and `Enable HTTPS`. If you try to access your app at the address propsed
(which should look like https://this-is-a-test-app.blog.yourdomain.com), you should see something like below.

[![saVDHF.md.jpg](https://iili.io/saVDHF.md.jpg)](https://freeimage.host/i/saVDHF)

### 4.2. Deploy your app

In a terminal run 

```shell
caprover deploy
```

And follow the steps:

```shell
(venv) PS > caprover deploy


Preparing deployment to CapRover...

? select the CapRover machine name you want to deploy to: captain-01
Ensuring authentication...
? select the app name you want to deploy to: this-is-a-test-app
? git branch name to be deployed: main
? note that uncommitted and gitignored files (if any) will not be pushed to server! Are you sure you want to
deploy? Yes

Build has finished successfully!

Deployed successfully this-is-a-test-app
App is available at https://this-is-a-test-app.blog.yourdomain.com
```

Bravo 👏👏 Your app should now be successfully deployed!!

### 4.3. Add environment variables

You should see something like this :

[![saWszG.md.jpg](https://iili.io/saWszG.md.jpg)](https://freeimage.host/i/saWszG)

Well, we're almost there... As described in the repo [`README`](https://github.com/kenshuri/django_tailwind_caprover), we need to modify our app environments variables.

To do so, go in the tab `App Configs` in CapRover, and use the bulk edit to create the environment variables.

```text
DJANGO_DEBUG=TRUE
DJANGO_SECRET_KEY=^a@fg8s132ksy00(ww9xc-vgi3v78om#$rh(a-(9)68a=zptk2
APP_ALLOWED_HOSTS=this-is-a-test-app.blog.yourdomain.com
```

Go to you app again. Do you see something like this?

[![sajlxs.jpg](https://iili.io/sajlxs.jpg)](https://freeimage.host/fr)

It could be for 2 reasons:

* You need to upload the CSS file
* You need to run `collectstatic` at deployment so that your static files are served to the server

### 4.4. Upload the CSS file

If the answer is yes, let's face it: this daisy button does not look at all like a [daisy button](https://daisyui.com/components/button/#button)!

The reason is quite simple: it's simply because we did not push the css file. After cloning the example repo, you should
create your own repo and push the css file. Here is the process I usually follow.

1. Create a new repo in Github, let's call it `test_app_cap`
2. Remove the current remote branch from the repo you juste cloned `git remote rm origin`
3. Finally push to your new repo
4. 
```shell
git remote add origin https://github.com/username/test_app_cap.git
git branch -M main
git push -u origin main 
```

Now, you should build the css file as described in the repo `README`

```shell
cd jstoolchains
npm run tailwind-build
```

A new file `blogApp/static/css/output.css` has been created. Commit and push it.

```shell
cd ..
git commit .\blogApp\static\css\output.css -m "update css"
git push origin
```

### 4.5. Run `collectstatic` at deployment

To run `collectstatic` at deployment, you need to tweak the `captain-definition` file that we created before.

The default `captain-definition` for a `python-django` app define a default list of commands to be executed at deployment. 
You can see these commands being executed (one step for each command) when you call `caprover deploy`.
Unfortunately, the `run collectstatic` is not part of these default commands. 
We thus need to define a custom deployment file ourselves, stating explicitly that we want to run `collectstatic`. 
To do so, we will create a custom `Dockerfile`!

#### 4.5.1 Modify `captain-definition` file

Change your current `captain-definition` file so that it does not use the default `django-python` list of commands
but refer to your custom dockerfile instead.

```text
captain-definition

 {
  "schemaVersion": 2,
  "dockerfilePath": "./Dockerfile"
 }
```

#### 4.5.2 Create custom `Dockerfile`

At the root of your project, create a custom `Dockerfile` as below:

```dockerfile
#Dockerfile

FROM library/python:3.10-alpine

RUN apk update && apk upgrade && apk add --no-cache make g++ bash git openssh postgresql-dev curl

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /usr/src/app

EXPOSE 80

# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
```

Each row of this `Dockerfile` corresponds to a command that was executed by default. 
You can check it against the steps executed when running `caprover deploy` before. 
There is only one addition: `RUN python manage.py collectstatic --noinput`

Now that this is done, you can commit, push and deploy again !

```shell
git commit .\blogApp\static\css\output.css -m "add Dockerfile"
git push origin
caprover deploy
```

Bravissimo 👏!! You have now deployed 🚀 a django app to your server using CapRover: bye-bye Heroku 👋👋!

## 5. Deploy a Django app with heavier dependencies

While everything is running perfectly at the moment, you could quickly face deployment issues if your were to add some heavier dependencies.
For instance, let's try to add `pandas` to your `requirements.txt` and deploy again.

```shell
pip install pandas
pip freeze > requirements.txt
git commit requirements.txt -m "add Pandas"
git push
caprover deploy
```

If as me, you took the cheapest server available on DigitalOcean with only 1GB of memory, there is a big chance that the 
deployment fails as this:

```shell
Collecting pandas==1.5.0
Downloading pandas-1.5.0.tar.gz (5.2 MB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2/5.2 MB 108.9 MB/s eta 0:00:00

Installing build dependencies: started
Installing build dependencies: still running...
Installing build dependencies: still running...
Installing build dependencies: still running...

Something bad happened while retrieving issue-app app build logs.
502 - "<html>\r\n<head><title>502 Bad Gateway</title></head>\r\n<body>\r\n<center><h1>502 Bad Gateway</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n"


Something bad happened while retrieving issue-app app build logs.
Error: connect ECONNREFUSED 164.92.140.20:443


Something bad happened while retrieving issue-app app build logs.
502 - "<html>\r\n<head><title>502 Bad Gateway</title></head>\r\n<body>\r\n<center><h1>502 Bad Gateway</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n"


Something bad happened while retrieving issue-app app build logs.
502 - "<html>\r\n<head><title>502 Bad Gateway</title></head>\r\n<body>\r\n<center><h1>502 Bad Gateway</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n"


Something bad happened while retrieving issue-app app build logs.
Captain is not ready yet...


Something bad happened while retrieving issue-app app build logs.
Captain is not ready yet...


Something bad happened while retrieving issue-app app build logs.
Captain is not ready yet...


Something bad happened while retrieving issue-app app build logs.
Error: connect ECONNREFUSED 164.92.140.20:443


Something bad happened while retrieving issue-app app build logs.
Error: connect ECONNREFUSED 164.92.140.20:443


Something bad happened while retrieving issue-app app build logs.
Error: connect ETIMEDOUT 164.92.140.20:443


Something bad happened while retrieving issue-app app build logs.
Captain is not ready yet...


Something bad happened while retrieving issue-app app build logs.
Captain is not ready yet...


Something bad happened while retrieving issue-app app build logs.
Password is incorrect.


Something bad happened while retrieving issue-app app build logs.
Password is incorrect.


Something bad happened while retrieving issue-app app build logs.
Password is incorrect.
```

What's happening here is that your server is running out of memory and the entire server crashes.

This a well known issue documented
- In this [github](https://github.com/caprover/caprover/issues/1507) issue
- In the [doc](https://caprover.com/docs/best-practices.html#out-of-memory-when-building)

The doc describes possible options below

> When you build on a paid service such as Heroku, your build process happens on a machine with high CPU and RAM. When you use CapRover, your build is done on the same machine that serves your app. This is not a problem until your app gets too big and the build process requires too much RAM. In that case, your build process might crash! See this for example. There are multiple solutions:
> 
> 1. Add swap space to the web server, explained here.
> 2. Build on your local machine. For example, this process is explained in detail here for Create React App.
> 3. However, the best solution is to use a separate build system. You can see the guide [here](https://caprover.com/docs/ci-cd-integration.html)
> 

However, there is a simpler one that I would like to introduce (solution 3 is also implemented later in this tutorial)!

The problem is that the building of the docker image takes a lot of time. 
The main reason for this is that we use the Alpine linux image. 
This issue is discussed in this [stackoverflow ticket](https://stackoverflow.com/questions/49037742/why-does-it-take-ages-to-install-pandas-on-alpine-linux) 
or in this very good [blog post](https://pythonspeed.com/articles/alpine-docker-python/).
To put it simply, Alpine Linux is usually a very good image to use, but not when packaging a Python application: it's better to use a Debian based image in such cases.
This [page](https://hub.docker.com/_/python) list several images available, we'll use the `slim` image!

Let's modify the `Dockerfile` accordingly:

```dockerfile
#Dockerfile

FROM python:3.10.8-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /usr/src/app

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
```

Finally, deploy again your app

```shell
caprover deploy
```

We're finally free from Heroku, and it works well! Moreover, now that you've deployed once, 
it's even faster than with Heroku to deploy again! 

## 6. Go full DevOps
To make your deployment even faster, we can follow Caprover doc advice, and implement a solution to build and deploy automatically from Github when a change happen on your main branch : how cool is that 😎 ??!!

The steps are

1. Enable App Token in your CapRover app configuration
2. Add Github Secrets
3. Create Github Action


### Enable App Token in your CapRover app configuration

*from [CapRover doc](https://caprover.com/docs/ci-cd-integration/deploy-from-github.html#enable-app-token)*

Find the "Deployment" tab for your new app, click Enable App Token and copy this token. This is your **`APP_TOKEN`** secret.

### Create a Personal Acces Token in Github

In your Github Settings, go to [Developer settings](https://github.com/settings/apps). Then, in Personal access tokens, 
[Generate a new classic token](https://github.com/settings/tokens/new) with scope: `write:packages`

### Add the Docker Registry in Caprover

On the caprover machine where your app is deployed, go to Cluster, and add your Remote Registry.

[![DCaHJe.md.jpg](https://iili.io/DCaHJe.md.jpg)](https://freeimage.host/i/DCaHJe)

### Add Github Secrets

Github secrets are variables used by Github when trying to deploy your app. You need to define several variables/secrets.

To define your Github Secrets, go in your repo Settings > Secrets > Actions

[![sbHZf2.md.jpg](https://iili.io/sbHZf2.md.jpg)](https://freeimage.host/i/sbHZf2)

And define the following repository secrets.

* CAPROVER_SERVER = https://captain.blog.yourdomain.com
* CAPROVER_PASSWORD = yourcaproverpassword
* APP_NAME = this-is-a-test-app
* PAT = PERSONAL_ACCES_TOKEN

### Create Github Action

Now, you need to tell Github that it should do something when a change happen on the main branch, and define what it should do.

This is done thanks to `.yml` that needs to live in a specific folder in your repo. Create a new file `.github/workflows/deploy.yml`

```yaml
#.github/workflows/deploy.yml

name: Publish to caprover

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
    
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:

  build:

    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Log in to the Container registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.PAT }}
        
    - name: Extract metadata (tags, labels) for Docker
      id: meta
      uses: docker/metadata-action@v4
      with:
        images:  ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

    - name: Build and push
      uses: docker/build-push-action@v3
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
    
    - name: Deploy image
      uses: floms/action-caprover@v1
      with:
        host: '${{ secrets.CAPROVER_SERVER }}'
        password: '${{ secrets.CAPROVER_PASSWORD }}'
        app: '${{ secrets.APP_NAME }}'
        image: ${{ steps.meta.outputs.tags }}

```

We're finally done !!

The final code is available [here](https://github.com/kenshuri/django_tailwind_caprover).