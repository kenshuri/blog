---
title: Deploy to CPanel - O2Switch
summary: Deploy a Django app to a standard VPS with CapRover
date: 2023-06-11
badge: code
image:
---

# Deployment from A to Z

## Buy host

**Steps**

1. Git clone project to kenshuri.com
2. Configure le domaine avec comme racine le dossiser cloné
3. Créer une application python
   - Application Root = kenshuri.com --> le dossier racine
   - Application URL kenshuri.com
   - Modifier le fichier kenshuri.com/passenger_wsgi pour qu'il pointe vers le bon fichier wsgi

```wsgi
import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'blogProject/wsgi.py')
application = wsgi.application
```

4. pip install requirements / pip install poetry --> poetry install
5. Restart app
6. If it does not work, check that blogProject/wsgi has correct value
7. makemigrations/migrate/collectstatic


