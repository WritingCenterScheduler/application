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
  
# Deployment:

This repo can be set to track to OpenShift.  Changes made to master then explicitly pushed to the wss remote.  Pushing to remote triggers reload of all cartridges and requirements.

# Authentication:

Because of how this is set up, all users hitting the app will be SSO authenticated.  

# Database

Create the admin local user - running in UNAUTHENTICATED MODE

```
use wss

db.createUser(
    {
        user: "local",
        pwd: "default",
        roles: [ "dbAdmin" , "read"]
    }
)

db.grantRolesToUser(
    "local",
    [
      { role: "read", db: "wss" }
    ]
)
```