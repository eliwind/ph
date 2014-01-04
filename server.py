from cherrypy import wsgiserver
import cherrypy
from cherrypy.process.plugins import Daemonizer
from ph import app

app.debug = True
d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), d)

if __name__ == '__main__':
   try:
      server.start()

   except KeyboardInterrupt:
      server.stop()

