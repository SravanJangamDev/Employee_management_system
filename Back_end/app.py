from wsgiref.simple_server import make_server
import falcon
import json

# import jwt
from sqldb import mysql_action
from user_routes import Login, Logout, Register
from employee_routes import EmployeeAction, EmployeesAction
from falcon.http_status import HTTPStatus


class AuthMiddleWare(object):
    def process_request(self, req, resp):
        path = req.path
        if path not in ["/", "/login", "/register"]:
            auth = req.get_header("Authorization")
            if auth is None or auth == "":
                raise falcon.HTTPUnauthorized(
                    title="Authorization required",
                    description="please enter the Authorization key",
                )

        try:
            role = req.get_header("role")
            if role != "admin":
                raise falcon.HTTPUnauthorized(
                    title="Authorization required", description="only admin can access"
                )
        except Exception as e:
            raise falcon.HTTPUnauthorized(
                title="Authorization required", description="only admin can access"
            )


class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Methods", "*")
        resp.set_header("Access-Control-Allow-Headers", "*")
        resp.set_header("Access-Control-Max-Age", 1728000)
        if req.method == "OPTIONS":
            raise HTTPStatus(falcon.HTTP_200, body="\n")


class Home:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"Employee": "Welcome to emplyee management system"})


app = falcon.API(middleware=[HandleCORS(), AuthMiddleWare()])
# app = falcon.App()
app.add_route("/", Home())
app.add_route("/employees", EmployeesAction())
app.add_route("/employee/{id}", EmployeeAction())
app.add_route("/login", Login())
app.add_route("/register", Register())
app.add_route("/logout", Logout())

if __name__ == "__main__" :
    with make_server("", 8005, app) as httpd :
        print("serving on port 8000.............")
        httpd.serve_forever()
