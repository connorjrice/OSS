import os
import sys

from collections import defaultdict
from astral.server import ASTServer, BaseHandler
from peak.backend import PBackend
from peak.component import ComponentFactory
import peak.handlers

class PeakServer(ASTServer):

    def __init__(self):
        super().__init__()
        self.port = 8667
        self.settings = {
            'backend' : PBackend(),
            'autoreload' : True,
            'static_path': self.find_static_files(),
            'debug': True,
            'login_url': '/',
        }

        components = {'/':  {'kind': 'login', 'nav': 'navlogin.html', 'handler': peak.handlers.LoginHandler, 'template': 'login'},
                      '/home' : {'kind': 'home'},
                      '/checkin': {'kind': 'checkin'},
                      '/admin': {'kind': 'admin'},
                      '/store': {'kind': 'cover'},
                      '/outreach': {'kind': 'cover'},
                      '/support': {'kind': 'support'},
                      '/shift': {'kind': 'cover'},
                      '/feedback': {'kind': 'feedback'},
                      '/login': {'kind': 'login'},
        }

        self.handlers = [ComponentFactory().get_handler(url, **kwargs) for url, kwargs in components.items()]

    def find_static_files(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'static')):
            return os.path.join(os.path.dirname(__file__), 'static')
        elif os.path.exists(os.path.join(os.getcwd(), 'static')):
            return os.path.join(os.getcwd(), 'static')
        else:
            raise FileNotFoundError(f'unable to find static files at {os.getcwd()}')

if __name__ == '__main__':
    app = PeakServer()
    if len(sys.argv) == 1:
        app.serve_local(cmd=True)
