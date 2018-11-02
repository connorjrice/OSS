import logging
import os
import sys

import traceback
import uuid

import tornado.ioloop
import tornado.web
import tornado.httpserver

class BaseHandler(tornado.web.RequestHandler):

    @property
    def backend(self):
        return self.application.settings['backend']

    def get_current_user(self):
        uid = self.get_secure_cookie('user')
        if not uid: return None
        return self.backend.get_user(uid)

    def xsrf(self, **dc):
        dc['xsrf'] = self.xsrf_token
        return dc

    def log(func):
        def _log(*args):
            #args[0].backend.log((args[0].request, args[0]))
            func(*args)
        return _log

    def gen_params(self):
        """Generate dict of parameters based upon request"""
        return {param: self.get_argument(param) for param in self.params}

    def render_unto_caesar(self, obj, tar=f'templates{os.sep}base.html'):
        #try:
        self.render(tar, **self.xsrf(obj(**self.gen_params()).get_params()))
        #except tornado.web.MissingArgumentError:
        #    self.render(tar, **self.xsrf(obj().get_params()))

    def render_unto_connor(self, obj, tar=f'templates{os.sep}base.html'):
        self.render(obj.template, **self.xsrf(**obj.params))

    @tornado.web.authenticated
    def render_secure(self, obj, tar=None):
        if not tar:
            self.render(obj.template, **self.xsrf(**obj.params))
        else:
            self.render(tar, **self.xsrf(**obj.params))

class ErrorHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            """
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })
            """
            
            #self.finish('kappa xd')
            self.redirect(f'https://http.cat/{status_code}')
    

class ASTServer(object):

    def __init__(self):
        super().__init__()
        self.default_settings = {
            "cookie_secret": str(uuid.uuid4()),
            "autoescape": None,
            "xsrf_cookies": True,
            'compiled_template_cache': False,
            'default_handler_class' : ErrorHandler,
        }
        self.default_handlers = []
        self.settings = {}
        self.handlers = []
        self.port = 8000

    def make_app(self):
        settings = {**self.default_settings, **self.settings}
        handlers = self.default_handlers + self.handlers
        return tornado.web.Application(handlers, **settings)

    def start_server(self, thread=False):
        if thread:
            ioloop = tornado.ioloop.IOLoop.instance()
            thread = threading.Thread(target=ioloop.start)
            thread.start()
            return (thread, ioloop, self.port)

    def serve_local(self, cmd=False):
        print(f'serving on localhost:{self.port}')        
        if not cmd:
            app = self.make_app()
            app.listen(port)
            self.start_server(port)
        else:
            try:
                app = self.make_app()
                app.listen(self.port)
                tornado.ioloop.IOLoop.current().start()
            except KeyboardInterrupt:
                tornado.ioloop.IOLoop.current().stop()

    def serve_ssl(self, thread=False, port=443, ssl_options=None):
        app = self.make_app()
        server = self.tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
        server.listen(port)
        self.start_server(thread, port)


