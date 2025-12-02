import mimetypes
import os
from jinja2 import Environment, FileSystemLoader
import DB_Handler
from urllib.parse import parse_qs

env = Environment(loader=FileSystemLoader('Template'))

def static(envir, start_response):
    """
    :param envir:
    :param start_response:
    :return: The static CSS if it is found
    """
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, "Template")

    path = str(envir.get("PATH_INFO", ""))
    if path.startswith("/static/"):
        rel_path = path[len("/static/"):]
        file_path = os.path.join(html_dir, "static", rel_path)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                style = f.read()
                start_response("200 OK", [("Content-Type", "text/css")])
                return [style]
        else:
            start_response("404 Not Found", [('Content-Type', 'text/plain')])
            return [b"File not found"]

def image(envir, start_response):
    """
    :param envir:
    :param start_response:
    :return: The static CSS if it is found
    """
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, "Template")

    path = str(envir.get("PATH_INFO", ""))
    if path.startswith("/Images/"):
        rel_path = path[len("/Images/"):]
        file_path = os.path.join(html_dir, "Images", rel_path)
        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"

            with open(file_path, "rb") as f:
                img = f.read()
                start_response("200 OK", [("Content-Type", mime_type)])
                return [img]
        else:
            start_response("404 Not Found", [('Content-Type', 'text/plain')])
            return [b"File not found"]

def simple_app(envir, start_response):

    path = envir.get("PATH_INFO", "/")
    if path == "/" or path == "":
        path = "/Home.html"

    ## Getting Filepath to make sure the html file exist
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, "Template")
    filename = path.lstrip("/")
    full_path = os.path.join(html_dir, filename)

    ## Used solely for CSS files
    static_response = static(envir, start_response)
    if static_response:
        return static_response

    img_response = image(envir, start_response)
    if img_response:
        return img_response

    team = ""
    ## Passing data to the html file
    if not os.path.exists(full_path):
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"404 Not Found"]
    if envir['REQUEST_METHOD'] == 'POST':
        try:
            size = int(envir.get('CONTENT_LENGTH', 0))
        except ValueError:
            size = 0
        body = envir["wsgi.input"].read(size)
        params = parse_qs(body.decode())
        team = params.get("team", [''])[0]

    with open(full_path, 'r', encoding="utf-8") as f:
        if filename == "Stats.html":
            players = DB_Handler.get_players(team)
            # player_stats = DB_Handler.get_players()
            template = env.get_template("Stats.html")
            html = template.render(players=players)
        else:
            html = f.read()

    start_response("200 OK", [("Content-type", "text/html")])
    return [html.encode("utf-8")]



