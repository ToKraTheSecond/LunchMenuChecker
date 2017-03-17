# Glip LunchMenuChecker for Python 3.5

Get menu from:
- BlackPoint
- Buddha
- GoldenNepal
- Sabaidy
- Osmicka

and post it to Glip conversation via Glip WebHooks.

Chinese fortune cookies source: http://www.fortunecookiemessage.com

Add your Glip webhook links to gliplinks.txt

Type of conversation (test/team) and restaurant is selected by two input parameteres during script call.

First argument is for conversation selection.

Test:
```
python lunchchecker.py t all
```

Team:
```
python lunchchecker.py o all
```
Second argument is for restaurant selection.

Restaurant selection:
```
python lunchchecker.py o all
python lunchchecker.py o GetMenuRestaurantname
```
