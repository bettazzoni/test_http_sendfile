#!/usr/bin/env python
import sys, base64

def send_file_via_put_http(source_file, dest_file, url='127.0.0.1:8080'):
    if sys.version_info[0] == 2:
        import httplib      
        h =  httplib.HTTPConnection(url)
    else:    
        import http.client
        h =  http.client.HTTPConnection(url)
    f = open(source_file, 'rb')
    source_bin_content = f.read()
    f.close()
    h.request(method='PUT', 
              url=dest_file, 
              body=base64.b64encode(source_bin_content), 
              headers={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" } )
    return h.getresponse().read()

source_filename = sys.argv[1] if len(sys.argv) > 1 else "taz.jpg"
destination_filename = sys.argv[2] if len(sys.argv) > 2 else "copy."+ source_filename
resp = send_file_via_put_http(source_filename, destination_filename)
if len(resp) > 0:
        print(resp)
