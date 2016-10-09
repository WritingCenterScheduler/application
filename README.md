# Engine

### Setup.

1. git clone the code.
2. create a virtualenv
  1. `mkdir venv`
  2. `cd venv`
  3. `virtualenv -p python3 .`
  4. `cd .. && source venv/bin/activate`
  5. `pip install -r requirements.txt`
3. run unit tests
  1. `python -m unittest discover`

# Encodings explained

* In employee preferences:
  * 2 == best
  * 1 == OK
  * 0 == bad

* In deciding which employees to schedule first:
  * higher "type" number determines precidence.  For example, if a type 1 employee is needed, they are scheduled before a type 0.