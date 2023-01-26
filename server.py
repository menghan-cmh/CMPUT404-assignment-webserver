#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK", 'utf-8'))
        self.data = self.data.decode(encoding='UTF-8',errors='strict').split()
        
        # print("===test===", data[0], "\n")

        if (len(self.data) == 0):
            return

        # self.data[0] <- method
        if (self.data[0] == "GET"):
            print("I can handle GET request...\n")
            self.handleGet()
            # self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
        else:
            # POST, PUT, DELETE etc.
            print("I cannot handle", self.data[0], "request...")
            self.createRequest("405 Method Not Allowed")
    
    def handleGet(self):
        # check if html/css file 
        content_type = ""
        
        check = self.data[1].split(".")[-1]
        print(check)
        if check == "html":
            content_type = "text/html"
        elif check == "css":
            content_type = "text/css"


        # host + path
        self.url = "http://" + self.data[4] + "/www" + self.data[1]
        # local directory
        self.path = "/www" + self.data[1]
        dir = os.getcwd() + "/www" + self.data[1]

        if (check != "html" and check != "css" and self.data[1][-1] != '/'):
            print("not end with /")
            self.url += '/'
            dir += '/'
            self.path += '/'
            print(self.path)
            print("end with /")
            self.createRequest("301 Moved Permanently", "text/html", self.url)

        if (self.path[-1] == '/'):
            print("======?????\n")
            self.url += "index.html"
            dir += "index.html"
            self.path += "index.html"
            print(self.path, "\n")

        try:
            self.createRequest("200 OK", content_type, self.path)
            print("200")
        except:
            self.createRequest("404 Not Found")
            print("404")

        
        print("\n")
        return
    
    def createRequest(self, status, content_type="text/html", path=None):
        f2 = ""

        try:
            f = open(path[1:])
            f2 = f.read()
            f.close()
        except:
            print("cannot find file")
        newRequest = "HTTP/1.1 " + status + "\r\n" + "Content-Type: " + content_type + "\r\n\r\n" + f2
        self.request.sendall(bytearray(newRequest, 'utf-8'))
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
