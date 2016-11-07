class User:

    def __init__(self,
        name="User",
        pid=-1,
        email="unknown",
        onyen="unknown",
        typecode="000"):

        self.name = name
        self.pid = pid
        self.email = email
        self.onyen = onyen
        self.typecode = typecode # An N digit number.
            # (0/1)XXXX... determines not admin/admin
            # X(0/1)XXX... determines new/returning
            # XX(0/1)XX... determines something else...?

    @property
    def is_admin(self):
        return self.typecode[0] == "1"

    @property
    def scalar_type(self):
        return self.typecode[1]

    def is_returner(self):
        return self.typecode[1] == "1"
