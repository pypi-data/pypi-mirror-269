import json
from cffi import FFI

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '1.0.5'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/javacommons/py-jsonffi'
__all__ = ['JsonFFI']

class JsonFFI:
    def __init__(self, dll):
        self.ffi = FFI()
        self.ffi.cdef("const char *Call(const char *, const char *);")
        self.ffi.cdef("const char *LastError();")
        self.clib = self.ffi.dlopen(dll)
    def call(self, name, args):
        answer = self.ffi.string(self.clib.Call(name.encode(), json.dumps(args).encode())).decode()
        error = self.ffi.string(self.clib.LastError()).decode()
        if error == "": return json.loads(answer)
        raise Exception(error)

class MyJS:
    def __init__(self, myjsDll, asmSpecList = []):
        self.api = JsonFFI(myjsDll)
        return self.api.call("Init", asmSpecList)
    def SetValue(self, name, value):
        return self.api.call("SetValue", [name, value])
    def GetValue(self, name):
        return self.api.call("GetValue", [name])
    def Execute(self, script, *vars):
        return self.api.call("Execute", [script, vars])
    def Evaluate(self, script, *vars):
        return self.api.call("Evaluate", [script, vars])
    def Call(self, name, *vars):
        return self.api.call("Call", [name, vars])

class MyCS:
    def __init__(self, mycsDll, asmSpecList = []):
        self.api = JsonFFI(mycsDll)
        return self.api.call("Init", asmSpecList)
    def Execute(self, script, *vars):
        return self.api.call("Execute", [script, vars])
    def Evaluate(self, script, *vars):
        return self.api.call("Evaluate", [script, vars])
    def Call(self, name, *vars):
        return self.api.call("Call", [name, vars])
