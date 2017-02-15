from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from my_html import base, my_form, main_content
from read_data import get_restaurants

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = get_restaurants()

                title = "Restaurants"
                item_list = ""
                for item in restaurants:
                    item_list += "<li> {} </li>".format(item.name)

                content = main_content.format(item_list)
                output = base.format(content=content, title=title)

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                title = "Hello!"
                content = hola_content
                output = base.format(content=content, title=title)
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                content = post_content.format(messagecontent, my_form)
                title = "POST stuff."
                output = base.format(content=content, title=title)
            self.wfile.write(output)
            print(output)

        except Exception as e:
            raise


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
