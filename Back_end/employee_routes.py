from sqldb import mysql_action
import json
import falcon
from user_routes import login


def valid_employee_params(req, resp, resource, params):
    data = req.media
    if (
        "name" not in data
        or "salary" not in data
        or "address" not in data
        or "designation" not in data
    ):
        msg = "please enter employee details properly"
        raise falcon.HTTPBadRequest(title="Bad request", description=msg)
    emp_name = data["name"]
    emp_designation = data["designation"]
    if emp_name == "" or emp_designation == "":
        msg = "employee name and designation should not be empty"
        raise falcon.HTTPBadRequest(title="Bad request", description=msg)


class Employee:
    def __init__(self, emp_id, emp_name, emp_salary, emp_address, emp_designation):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.emp_salary = emp_salary
        self.emp_designation = emp_designation
        self.emp_address = emp_address


class EmployeeAction:
    def on_get(self, req, resp, id):
        login(req, resp)
        resp.status = falcon.HTTP_200
        query = "select * from employees where id = {}".format(id)
        cur = mysql_action(query, "fetch employee details")
        data = json.dumps({"employee": {}})
        for emp in cur:
            e_dict = {
                "emp_id": emp[0],
                "emp_name": emp[1],
                "emp_salary": emp[2],
                "emp_address": emp[3],
                "emp_designation": emp[4],
            }
            data = json.dumps({"employee": e_dict})
            break
        else:
            raise falcon.HTTPBadRequest(
                title="Bad request",
                description="Employee with {} does not exist".format(id),
            )
        resp.body = data

    @falcon.before(valid_employee_params)
    def on_put(self, req, resp, id):
        login(req, resp)
        resp.status = falcon.HTTP_200
        data = req.media
        emp_id = id
        emp_name = data["name"]
        emp_salary = data["salary"]
        emp_designation = data["designation"]
        emp_address = data["address"]
        query = "update employees set name = '{}', salary = {}, address = '{}', designation = '{}' where id = {};".format(
            emp_name, emp_salary, emp_address, emp_designation, emp_id
        )
        mysql_action(query, "update employee")
        resp.body = json.dumps(data)

    def on_delete(self, req, resp, id):
        login(req, resp)
        resp.status = falcon.HTTP_200
        query = "select * from employees where id = {};".format(id)
        cur = mysql_action(query, "delete employee")
        data = json.dumps({"employee": {}})
        for emp in cur:
            e_dict = {
                "emp_id": emp[0],
                "emp_name": emp[1],
                "emp_salary": emp[2],
                "emp_address": emp[3],
                "emp_designation": emp[4],
            }
            data = json.dumps({"employee": e_dict})
            break
        else:
            raise falcon.HTTPBadRequest(
                title="Bad request",
                description="Employee with id {} does not exist".format(id),
            )
        query = "delete from employees where id={};".format(id)
        mysql_action(query, "delete employee")
        resp.body = data


class EmployeesAction:
    def on_get(self, req, resp):
        login(req, resp)
        resp.status = falcon.HTTP_200
        query = "select * from employees;"
        cur = mysql_action(query, "fetch employee details")
        emp_dict = []
        for emp in cur:
            e_dict = {
                "emp_id": emp[0],
                "emp_name": emp[1],
                "emp_salary": emp[2],
                "emp_address": emp[3],
                "emp_designation": emp[4],
            }
            emp_dict.append(e_dict)
        resp.body = json.dumps({"employees": emp_dict})

    @falcon.before(valid_employee_params)
    def on_post(self, req, resp):
        login(req, resp)
        resp.status = falcon.HTTP_200
        data = req.media
        emp_name = data["name"]
        emp_salary = data["salary"]
        emp_designation = data["designation"]
        emp_address = data["address"]
        query = "insert into employees values (NULL,'{}',{},'{}','{}');".format(
            emp_name, emp_salary, emp_address, emp_designation
        )
        mysql_action(query, "new employee creation")
        resp.body = json.dumps(data)
