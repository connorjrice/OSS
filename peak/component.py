import astral.component
import astral.server
from tornado.template import Template

import os

class ComponentHandler(astral.server.BaseHandler):

    def initialize(self, **kwargs):
        self.component = Component(**kwargs)        
    
    def get(self):
        self.render_secure(self.component)

    def post(self):
        self.render_secure(self.component)

class ComponentFactory(object):

    def get_handler(self, url, **kwargs):
        """Return a handler to be packaged with tornado app"""
        if kwargs.get('handler', 0) == 0:
            return (rf'{url}', ComponentHandler, self.get_dict(**kwargs))
        else:
            return (rf'{url}', kwargs['handler'], self.get_dict(**kwargs))

    def get_dict(self, **kwargs):
        """Default values if desired"""
        result = kwargs
        if not kwargs.get('kind'):
            result['kind'] = 'default'
        return result

class Component(astral.component.Component):

    def __init__(self, **kwargs):
        """They're not alive yet, but they will be"""
        super().__init__()
        self.project_name = 'peak'
        self.template_path = self.get_template_path()
        if kwargs.get('template'):
            self.template = self.get_template(f'{kwargs["template"]}.html')
        else:
            self.template = self.get_template('base.html')

        title = 'Peak Internal-alpha'       
        default_titles = {'admin' : 'Admin view'}

        if kwargs.get('nav'):
            nav = self.read_file(self.get_template(f'{kwargs["nav"]}'))            
        else:
            nav = self.read_file(self.get_template('nav.html'))            

        if kwargs.get('css'):
            css = self.get_css(f'{kwargs["css"]}.css')
        else:
            css = self.get_css(f'{kwargs["kind"]}.css')

        bs4 = self.read_file(self.get_template(f'{kwargs["kind"]}.html'))

        self.default_params.update({
            'title' : title,
            'nav'  : nav,
            'bs4': bs4,
            'css' : css,
        })

        self.params = self.default_params

        if kwargs.get('render'):
            self.default_params['bs4'] = self.render_string(self.get_template(self.get_template(f'{kwargs["kind"]}.html')), self.default_params)

    def get_component(self, kind):
        return 

    def get_components(self):
        #return [getattr(self, func)() for func in self.components]
        ...

    def get_class(self, tar):
        pass

