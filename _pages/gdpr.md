---
layout: page
permalink: /gdpr/
title: Data Usage
---

## What technologies do you use for this website

This blog is built with the Jekyll static site generator framework and based on the [reverie](https://jekyllthemes.io/theme/reverie) theme.

The Jekyll framework generates a static website that contains 

* JavaScript
* HTML
* CSS
* Static assets such as images

Thus, this website runs purely in your browser. 
**No personal data** can-/will be stored on our server or any data base. 

## Where is the website hosted?

We use the Github Pages hosting service. You can find out more about the Github data protection guidelines [here](https://docs.github.com/en/github/site-policy/github-privacy-statement).

## Cookies

This site uses a few Cookies to enable third party plugins.

**All site cookies** use the `secure;samesite=strict` cookie flags.

* `samesite=strict` - makes sure that the cookie **cannot get used** by **other websites**

* `secure` - ensures that the cookie can **only be transferred** through **HTTPS**.

The following cookies get set when you approve the cookie consent dialog.

* `_ga` and `_ga_XXXXXX` (string) - provides the google analytics plugin with the tracking id of this blog.

* `cookie-notice-dismissed` (boolean) - gets set to `true` when the user accepted the cookie consent dialog. (we don't set this cookie if you don't confirm the cookie consent).

## Third Party Plugins

We use the following third party plugins

### Google analytics

Google Analytics is a statistics tool for websites.
We use the tool to analyze how many users visit our blog.

The tool provides also some localization data such as the region of the visitor.
It is my understanding that this localization data gets derived from the visitors IPv4 address.

In practice, this IPv4 is most likely the address of your NAT (e.g. router).

We configured "identify users by device" in the Google Analytics backend.
Thus, users are **not** identified by their id which would make cross-platform tracking possible.

You can read more about cross-platform tracking [here](https://support.google.com/analytics/answer/9213390?hl=en&utm_id=ad)

Your tracking information has a **retention** time of **two months**.

Please contact me under dennis.gross@betteratpython.com if you wish a manual deletion of your tracking data.