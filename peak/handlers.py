import astral.server
import peak.component
import pandas

class LoginHandler(peak.component.ComponentHandler):

    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        self.target_component = peak.component.Component(**{'kind': 'support'})

    def get(self):
        self.render_unto_connor(self.component)

    def login(self, un, pw):
        if self.backend.auth_check(un, pw):
            self.set_secure_cookie("user", un)
            self.write("<html><script>window.alert('Login successful')</script></html>")
            self.render_unto_connor(self.target_component)
        else:
            self.write("<html><script>window.alert('Login unsuccessful')</script></html>")
            self.render_unto_connor(self.component)

    def post(self):
        self.login(self.get_argument('email'), self.get_argument('password'))

class AdminHandler(astral.server.BaseHandler):
    """Support a number of different check-in physical methods
    but initially for barcode
    """

    def initialize(self, **kwargs):
        super.initialize(**kwargs)
        self.clients_table = pandas.read_sql('select * from clients', self.backend.cx)
    
    def get(self):
        component = cpt.Component(kind='admin')
        self.render(component.template, **self.xsrf(**component.params))

'''
class CheckInHandler(astral.server.BaseHandler):
    """Support a number of different check-in physical methods
    but initially for barcode
    """
    def get(self):
        component = cpt.Component(kind='admin')
        self.render(check_in.template, **self.xsrf(**check_in.params))

class OutreachHandler(astral.server.BaseHandler):
    """Support a number of different check-in physical methods
    but initially for barcode
    """
    def get(self):
        component = cpt.Component(kind='admin')        
        self.render(outreach.template, **self.xsrf(**outreach.params))

class StoreHandler(astral.server.BaseHandler):
    """Support a number of different check-in physical methods
    but initially for barcode
    """
    def get(self):
        component = cpt.Component(kind='admin')        
        self.render(store.template, **self.xsrf(**store.params))

class StatusHandler(astral.server.astral.server.BaseHandler):

    def get(self):
        component = cpt.Component(kind='admin')        
        self.render(status.template, **self.xsrf(**status.params))

class SupportHandler(astral.server.BaseHandler):
    """Support a number of different check-in physical methods
    but initially for barcode
    """
    def get(self):
        component = cpt.Component(kind='admin')
        self.render(admin.template, **self.xsrf(**admin.params))

"""
(r'/', home.HomeHandler),
(r'/checkin', check_in.CheckInHandler),
(r'/admin', admin.AdminHandler),
(r'/help', status.StatusHandler),
(r'/store', pos.StoreHandler),
(r'/outreach', outreach.OutreachHandler),
(r'/outreach', outreach.OutreachHandler),            
#(r'/members', members.MemberHandler),                        
"""
'''
