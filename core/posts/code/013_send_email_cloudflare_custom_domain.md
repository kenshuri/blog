---
title: Send email using Cloudflare Custom Domain
summary: Use Mailjet to send email using an email adress defined in Cloudflare
date: 2025-03-02
badge: code
image:
---

# Send email using Cloudflare Custom Domain

To send emails using a **custom domain managed on Cloudflare**, follow these steps:

## **1. Choose an Email Sending Service**

I used Mailjet because it's a performant French solution, it was super easy to set-up.

- Mailjet (France) 🇫🇷
  - HQ: Paris, France
  - Features:
    - SMTP relay & API
    - Transactional & marketing emails
    - Advanced analytics & A/B testing
  - Pricing: Free tier (6,000 emails/month), paid plans start at ~€15/month
  - Website: https://www.mailjet.com

## **2. Configure your Email Sending Service**

- Create account
- Configure domain by creating a TXT DNS entry (see [help](https://documentation.mailjet.com/hc/fr/articles/360042561594-Comment-valider-un-domaine-d-envoi-en-int%C3%A9gralit%C3%A9))
- Configure SPF by creating a TXT DNS entry (see [help](https://documentation.mailjet.com/hc/fr/articles/360049641733-Guide-complet-d-authentification-des-domaines-avec-SPF-et-DKIM))
- Configure DKIM by creating a TXT DNS entry (see [help](https://documentation.mailjet.com/hc/fr/articles/360049641733-Guide-complet-d-authentification-des-domaines-avec-SPF-et-DKIM))
- Add an Sender Address from your [dashboard](https://app.mailjet.com/account/sender)
- Get Your API Keys from this [page](https://app.mailjet.com/account/apikeys) (see [help](https://documentation.mailjet.com/hc/fr/articles/360043229473-Comment-dois-je-configurer-mes-param%C3%A8tres-SMTP))

## **3. Configure Django**

Add the below in your `settings.py` file.

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "in-v3.mailjet.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-mailjet-api-key"  # Replace with your API Key
EMAIL_HOST_PASSWORD = "your-mailjet-secret-key"  # Replace with your Secret Key
DEFAULT_FROM_EMAIL = "your-email@example.com"  # Use an email associated with your domain
```

You're ready to go! 

## **4. Receive email to your custom domain** 

Has to be done in Cloudflare

- Set-up domain 
  - It will add several DNS entries: one of them is in conflict with the one used for SPF configuration
  - Accepts the changes: it will break the SPF configuration
  - Go to MailJet
  - Check the SPF configuration: it proposes a change, that adds the MailJet SPF on top of the Cloudflare
    - As in `"v=spf1 include:spf.mailjet.com include:_spf.mx.cloudflare.net ~all"`
- Back in Cloudflare, Email Routing
  - Check Destination Adress: You should see your domain
- In Cloudflare, Règles d'acheminement
  - Create a Custom Adress

You're done !