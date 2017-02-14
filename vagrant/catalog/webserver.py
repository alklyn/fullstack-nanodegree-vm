from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><title>Well Hello</title><body> Hello! </body></html>"
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()



if __name__ == '__main__':
    main()
