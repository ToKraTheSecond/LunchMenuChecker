# Glip Lunch Menu Checker
This script sends parsed restaurant lunch menu to given glip conversation via RingCentral Webhooks.
Tested with Python 3.6.

# What is glip?
[RingCentral Glip](https://glip.com) is a free team messaging app

# Installation
#### WIN machine
* clone this repo
* install dependencies via [conda/miniconda](https://www.anaconda.com/) with:
```
conda env create -f dependencies.yml
```
* add glip webhooks links to:
```
json_files/glip_links.json
```

# How to post
* call via terminal: *python lunch_menu_checker.py --type post_conv*

# Currently supported restaurants
* [Nepal Brno](http://nepalbrno.cz/)


