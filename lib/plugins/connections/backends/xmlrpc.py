import SimpleXMLRPCServer

import lib.aiml.configFile
import backend

# This string needs to be defined for each back end.  It should
# contain the name of the back-end class defined in this module.
backEndClass = "BackEndXMLRPC"

# default config file values for this module
configDefaults = {
	"xmlrpc.active":			"no",
	"xmlrpc.port":			    "8000"
	}

class BackEndXMLRPC(backend.IBackEnd):
    def __init__(self):
        config = lib.aiml.configFile.get()
        try: self._port = int(config['xmlrpc.port'])
        except: self._port = int(configDefaults['xmlrpc.port'])
        self._server = SimpleXMLRPCServer.SimpleXMLRPCServer(("", self._port), logRequests=0)
        respond = lambda input,user: self.submit(input,user+"@XMLRPC")
        respond.__doc__ = """Returns the bot's response to the 'input' string.
The 'user' string contains an ID the user making the request.
It is used internally as a unique session identifier for the user's conversation.
"""
        self._server.register_function(respond, "respond") 
        # This function is only available in fairly recent Python versions.
        try:
            self._server.register_introspection_functions()
        except:
            pass
        
    def go(self):
        self._server.serve_forever()
