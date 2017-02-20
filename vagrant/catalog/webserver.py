from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from insert_data import add_restaurant
from my_html import base, new_restaurant_form, main_content, item_html
from my_html import edit_restaurant_form
from my_html import add_new_content, my_js

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = \
                    session.query(Restaurant).order_by(Restaurant.name)

                title = "Restaurants"
                item_list = ""
                for item in restaurants:
                    item_list += item_html.format(
                        restaurant_name=item.name, restaurant_id=item.id)

                content = main_content.format(item_list)
                output = base.format(content=content, title=title, my_js="")

                self.wfile.write(output)
                # print(output)
                return

            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                title = "Add new restaurant!"
                content = new_restaurant_form
                output = base.format(content=content, title=title, my_js="")
                self.wfile.write(output)
                # print(output)
                return

            elif self.path.endswith("edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant_id = str(self.path).split("/")[-2]
                print(restaurant_id)

                if restaurant_id.isdigit():
                    restaurant_id = int(restaurant_id)
                    restaurant = \
                        session.query(Restaurant).filter(
                            Restaurant.id == restaurant_id).first()
                    if restaurant:
                        title = "Edit restaurant!"
                        content = edit_restaurant_form.format(
                            old_name=restaurant.name,
                            restaurant_id=restaurant.id)
                        output = base.format(
                            content=content, title=title, my_js="")
                        self.wfile.write(output)
                        # print(output)
                        return

                self.send_error(500, "Something went wrong.")

        except Exception as error:
            print("Error: {}".format(error))
            self.send_error(404, "File Not Found. {}".format(self.path))

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
                return

            if self.path.endswith("/restaurants/edit_restaurant"):

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('new_name')[0]
                    restaurant_id = fields.get('restaurant_id')[0]

                if restaurant_id.isdigit():
                    restaurant_id = int(restaurant_id)
                    restaurant = \
                        session.query(Restaurant).filter(
                            Restaurant.id == restaurant_id).first()

                    if restaurant and new_name:
                        print("Editing restaurant: {}".format(restaurant.name))
                        restaurant.name = new_name
                        session.add(restaurant)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants') # redirect
                        self.end_headers()
                        return

            self.send_error(500, "Something went wrong.")

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
