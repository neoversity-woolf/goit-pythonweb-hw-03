import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import urllib.parse
from jinja2 import Environment, FileSystemLoader
import json
import logging

JSON_FILE_PATH = "storage/data.json"

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())

        form_data = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }

        username = form_data.get("username")
        message = form_data.get("message")

        if username and message:
            self.save_to_json(username, message)
            print("Message sent successfully!")

        # Error after send data
        self.send_response(303)
        self.send_header("Location", "/message")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            self.render_read_page()
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def save_to_json(self, username, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        new_entry = {timestamp: {"username": username, "message": message}}

        try:
            with open(JSON_FILE_PATH, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data.update(new_entry)

        with open(JSON_FILE_PATH, "w") as file:
            json.dump(data, file, indent=2)

    def render_read_page(self):
        try:
            with open(JSON_FILE_PATH, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        template_env = Environment(loader=FileSystemLoader(searchpath="./"))
        template = template_env.get_template("read.html")
        logging.info("Render template %s", template)
        html_output = template.render(data=data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_output.encode())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        logging.info("Server started")
        logging.info("Listening port: %s", server_address[1])
        logging.info("Press CTRL + C to stop the server")
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
