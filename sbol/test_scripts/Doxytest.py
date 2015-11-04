## @file Doxytest.py
# Implements a high-level, Pythonic interface for the SWIG-Python classes in libsbol
# @package sbol
# A Python wrapper for libSBOLc, a module for reading, writing, and constructing
# genetic designs according to the standardized specifications of the Synthetic Biology Open Language

def test():
    return 0

## A dummy class for testing
class Doxytest_class(object):
    # uri method
    def uri(self):
        return self._uri
    def set_uri(self, value):
        self._uri = value
        return
    ## URI attribute
    uri = property(uri)
    uri = uri.setter(set_uri)
    ## Constructor
    def __init__(self):
        ## A generic attribute
        self.attr = None
        self._uri = None
        self.uri = Doxytest_class.uri


        ## URI attribute
        self.uri = Doxytest_class.uri

    @property
    def uri(self):
        return 0

    @uri.setter
    def uri(self, value):
        return 1




