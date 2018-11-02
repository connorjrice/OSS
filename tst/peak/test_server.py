import unittest
from peak.server import PeakServer

class TestSever(unittest.TestCase):

    def setUp(self):
        self.server = PeakServer()
    
    def test_initialization(self):
        self.server.make_app()

    def test_local_server(self):
        #self.server.serve_local()
        ...

    def test_find_components(self):
        pass

    def test_handler(self):
        pass
        
