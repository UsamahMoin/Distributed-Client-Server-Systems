
from xmlrpc.server import SimpleXMLRPCServer
import logging
from socketserver import ThreadingMixIn
import server_fns

class SimpleThreadedXMLRPCServer(ThreadingMixIn,SimpleXMLRPCServer):
    pass

server = SimpleThreadedXMLRPCServer(('localhost', 3000), logRequests=True, allow_none=True)

server.register_instance(server_fns.FileServer())

if __name__ == '__main__':

    try:
        logging.info('SERVER STARTED WORKING')
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('SERVER EXITTED DUE TO KEYBOARD INTERRUPT')
