import app
import wsgiref.simple_server as simple

if __name__ == "__main__":
    port = 8000
    with simple.make_server("", port, app.simple_app) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()
