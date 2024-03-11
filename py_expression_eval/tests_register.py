#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
#
# Based on js-expression-eval, by Matthew Crumley (email@matthewcrumley.com, http://silentmatt.com/)
# https://github.com/silentmatt/js-expression-eval
#
# Ported to Python and modified by Vera Mazhuga (ctrl-alt-delete@live.com, http://vero4ka.info/)
#
# You are free to use and modify this code in anyway you find useful. Please leave this comment in the code
# to acknowledge its original source. If you feel like it, I enjoy hearing about projects that use my code,
# but don't feel like you have to let me know or ask permission.

import unittest
import inspect
from py_expression_eval import Parser
from functools import wraps

class Funcies():
    engine_functions = {}

# https://www.pythontutorial.net/advanced-python/python-decorator-arguments/
def register_dtr( func):
    # def magic( *args, **kwargs ) :
        # #print "start magic"
        # result = func( *args, **kwargs )
        # #print "end magic"
        # return result
    print(f" registering {func}")    
    Funcies.engine_functions[func.__name__] = func
    return func  

class BaseEngine():

    @register_dtr
    def base_rating(self, url):
        rate = {"wibble.com" : "flooby",
                "grumble.com"  : "grumble",
                "flooby.com" : "flooby", }
        return rate[url]
class Engine(BaseEngine):

    def functions(self):
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        return members
        
    @register_dtr
    def referer_f(self, url):
        return 5

    @register_dtr
    def files_f(self, url):
        return 3
    
    @register_dtr
    def rating_f(self, url):
        rate = {"wibble.com" : "wibble",
                "grumble.com"  : "grumble",
                "flooby.com" : "flooby", }
        return rate[url]

    @register_dtr
    def buckets(self, url):
        cats = {"unknown.com" : [153],
                "grumble.com"  : [1,2,3],
                 "flooby.com" : [1,2,3], 
                }
        return set(cats[url])

class EngineTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.engine = Engine()
        self.engine_funcs = {}
        #for func_name, funcy in self.engine.functions():
        for func_name, funcy in Funcies.engine_functions.items():    
            print(f"func_name {func_name}")
            # https://stackoverflow.com/questions/2137539/how-to-invoke-a-method-that-has-been-discovered-through-inspect-getmembers
            self.engine_funcs[func_name] = getattr(self.engine,func_name)
            # self.engine_funcs
        # self.availabe_funcs = self.engine.functions()

    def test_engine(self):
       #  m = self.engine.functions()
        
        parser = Parser()
        url = "wibble.com"
        self.engine_funcs['url']= url
        res = parser.parse('(4 < referer_f(url)) or (4 < files_f(url)) or rating_f(url) in ("grumble")').evaluate(self.engine_funcs)
        assert True == res

        url = "grumble.com"
        self.engine_funcs['url']= url
        res =parser.parse('rating_f(url) in ("grumble")').evaluate(self.engine_funcs)
        assert True == res

        self.engine_funcs['url']= "flooby.com"
        res =parser.parse('rating_f(url) == "flooby"').evaluate(self.engine_funcs)
        assert True == res

        self.engine_funcs['url']= "grumble.com"
        res =parser.parse('base_rating(url) in ("flooby","grumble")').evaluate(self.engine_funcs)
        assert True == res
        res =parser.parse('1 < len(buckets(url))').evaluate(self.engine_funcs)
        assert True == res
if __name__ == '__main__':
    unittest.main()
