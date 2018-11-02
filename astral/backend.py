import astral.mixins

class Backend(astral.mixins.odbc, astral.mixins.auth):

    def __init__(self):
        super().__init__()
        self.path = 'base.db'
        self.user_table = 'users'
