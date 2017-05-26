# Glip LunchMenuChecker for Python 3

Get menu from:
- BlackPoint
- Buddha
- GoldenNepal
- Sabaidy
- Osmicka

restaurants and post it to Glip conversation via Glip WebHooks.

Chinese fortune cookies source: http://www.fortunecookiemessage.com

# Install

Add your Glip webhook links to gliplinks.txt

Install dependencies by:
```
pip install -r requirements.txt
```

# How to use

Type of conversation (test/team) and restaurant is selected by two input arguments during script call.

First argument is for conversation selection.

Test:

t - test
```
python lunchchecker.py t all
```

Team:

o - obedy
```
python lunchchecker.py o all
```
Second argument is for restaurant selection:

```
python lunchchecker.py o all
python lunchchecker.py o GetMenuRestaurantname
```
