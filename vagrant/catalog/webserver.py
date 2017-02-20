from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from my_html import base, new_restaurant_form, main_content, item_html
from my_html import add_new_content, my_js
from read_data import get_restaurants
from insert_data import add_restaurant

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
                    item_list += item_html.format(item.name)

                content = main_content.format(item_list)
                output = base.format(content=content, title=title, my_js="")

                self.wfile.write(output)
                print(output)
                return

            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                title = "Add new restaurant!"
                content = new_restaurant_form
                output = base.format(content=content, title=title, my_js="")
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/add_new"):

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('new_restaurant')[0]

                    add_restaurant(name)
                    print(name)

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants') # redirect
                self.end_headers()

        except Exception as e:
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
