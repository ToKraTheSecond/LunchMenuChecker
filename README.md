# Glip LunchMenuChecker for Python 3

Get menu from:
- BlackPoint
- Buddha
- GoldenNepal
- Sabaidy
- Osmicka
- TriOcasci
- Ponava
- BishesGurkha

restaurants and post it to Glip conversation via Glip WebHooks.

Chinese fortune cookies source: http://www.fortunecookiemessage.com and local txt file.

# Install

Add your Glip webhook links to gliplinks.txt

Install dependencies by:
```
pip install -r requirements.txt
```

# How to use

Type of conversation (test/team) and posting function is selected by two input arguments during script call.

First argument is for conversation selection.

Test:

t - test
```
python lunchchecker.py --type t --postfunc all
```

Team:

o - obedy(lunch)
```
python lunchchecker.py --type o --postfunc all
```
Second argument is for posting function selection:

```
python lunchchecker.py --type o --postfunc all
python lunchchecker.py --type o --postfunc func_name
```

# License
Project is licenced under GNU GPLv3 License
