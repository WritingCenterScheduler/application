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

`mongorestore -d [your_db_name] [your_dump_dir] `

Create the admin local user - running in UNAUTHENTICATED MODE

```
use wss

db.createUser(
    {
        user: "local",
        pwd: "default",
        roles: [ "dbAdmin" , "readWrite"]
    }
)

db.grantRolesToUser(
    "local",
    [
      { role: "root", db: "wss" }
    ]
)
```

Create a user for the application (this is not a mongo user)

```
db.user.insert({
  "pid": 111111111,
  "first_name": "Tar",
  "last_name": "Heel",
  "email": "user@unc.edu",
  "typecode": "110",
})
```

# Development:

To develop:
1. Start the mongo server in authenticated mode `sudo mongod --auth`
2. Start the flask server in dev mode. `
