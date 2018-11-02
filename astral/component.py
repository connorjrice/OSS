import os

class Component(object):

    def __init__(self):
        self.project_name = ''
        self.default_params = {
            'footer': 'undef software internal alpha &copy 2017',
        }

    def generate_dropdown(self):
        pass

    # pathing

    def get_template_path(self):
        return os.path.abspath(f'{self.project_name}{os.sep}templates{os.sep}') + os.sep

    def get_static_path(self):
        return os.path.abspath(f'{self.project_name}{os.sep}static{os.sep}') + os.sep

    def get_static(self, target):
        #path = os.path.join(os.path.abspath(f'.{os.sep}{self.project_name}'), target)
        path = f'.{os.sep}{self.project_name}{os.sep}{target}'
        with open(path, 'r') as target_file:
            return target_file.read()

    def read_file(self, path):
        with open(path, 'r') as target:
            return target.read()

    def get_template(self, template):
        #return os.path.join(self.template_path, template)
        return f'{self.template_path}{template}'

    def get_static(self, static):
        return f"{os.path.abspath(f'{self.project_name}{os.sep}{static}')}{os.sep}"

    def get_css(self, css):
        #return f"{os.path.abspath(f'{self.project_name}{os.sep}static{os.sep}css{os.sep}{css}')}"
        return f'"/static/css/{css}"'                

        
