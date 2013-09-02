#Copyright Jon Berg , turtlemeat.com

import cgi,time, os, logging, base64
from http.server import BaseHTTPRequestHandler, HTTPServer

log = logging.getLogger()

def dirlist(directory_path=os.curdir, filename_separator = "<br>\n"):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(directory_path) if isfile(join(directory_path,f)) ]
    return filename_separator.join(onlyfiles)

class MyHandler(BaseHTTPRequestHandler):
    
    def respond_ok(self, response_str=''):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if len(response_str) > 0:
            self.write_response(response_str)
    
    def write_response(self, response_str):
        rs =  '<head> <meta http-equiv="refresh" content="5" > </head>'+\
              '<body><html>'+response_str+'</html></body>'
        self.wfile.write(rs.encode())

    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                fname = os.path.abspath(os.path.join(os.curdir, os.path.basename(self.path)))
                with open(fname, 'rb') as f:  
                    self.respond_ok( f.read() )
            elif self.path == "/ls":                
                self.respond_ok(time.asctime() + '<br><h2>Dir ".":</h2><br>' + dirlist())
            return            
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_PUT(self): 
        fname = os.path.abspath(os.path.join(os.curdir, os.path.basename(self.path)))      
        file_dim = int(self.headers.get('Content-Length', 0))
        if file_dim > 0 and len(fname) > 2:
            fc = base64.b64decode(self.rfile.read(file_dim))
            log.info("file_name='%s' file_dim=%d", fname, len(fc) )
            with open(fname, 'wb') as f:
                f.write(fc)
        self.respond_ok()
        return

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print ("filecontent" + upfilecontent[0])
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass

def main():
    try:
        server = HTTPServer(('', 8080), MyHandler)
        print ('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()

