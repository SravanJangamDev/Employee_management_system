from sqldb import mysql_action
import json
import falcon
import bcrypt

# import jwt
import uuid
import time
import redis

redis_cli = redis.Redis(host = "localhost", port = 6379, db = 0)


def validate_user_params(req, resp, resource, params):
    credentials = req.media
    if "username" not in credentials or "password" not in credentials:
        msg = "please enter username and password properly"
        raise falcon.HTTPBadRequest(title="Bad request", description=msg)
    if credentials["username"] == "" or credentials["password"] == "":
        msg = "username and password should not be empty"
        raise falcon.HTTPBadRequest(title="Bad request", description=msg)


class User:
    def __init__(self, user_id, username, password, session_id, session_time):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.token = token
        self.token_time = token_time


class Register:
    @falcon.before(validate_user_params)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        credentials = req.media
        username = credentials["username"]
        password = credentials["password"]
        password = password.encode("utf-8")
        salt = bcrypt.gensalt(5)
        password = bcrypt.hashpw(password, salt).decode("utf-8")
        salt = salt.decode("utf-8")
        token = "55558058dggg2335215365"
        token_time = 4567373
        query = "insert into users values(NULL, '{}','{}', '{}', {}, '{}')".format(
            username, password, token, token_time, salt
        )
        mysql_action(query, "registration")
        resp.body = json.dumps({"registration": "successfully registered"})


class Login:
    @falcon.before(validate_user_params)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        credentials = req.media
        username = credentials["username"]
        password = credentials["password"]
        entered_password = password.encode("utf-8")
        query = "select * from users"
        cur = mysql_action(query, "login")
        for user in cur:
            actual_password = user[2].encode("utf-8")
            salt = user[5].encode("utf-8")
            user_hash = bcrypt.hashpw(entered_password, salt)
            actual_hash = bcrypt.hashpw(actual_password, salt)
            valid_pwd = bcrypt.checkpw(user_hash, actual_hash)
            if user[1] == username and valid_pwd:
                jwt_secret_key = uuid.uuid4().hex
                payload = {"user-id": user[0], "username": username}
                # token = jwt.encode(payload, jwt_secret_key, "HS256").decode("utf-8")
                token = jwt_secret_key
                token_time = time.time()
                query = "update users set token = '{}' , token_time = {} where id = {} ".format(
                    token, token_time, user[0]
                )
                mysql_action(query, "login")
                resp.set_header("token", token)
                break
        else:
            raise falcon.HTTPUnauthorized(
                title="Login failed", description="Invalid username or password"
            )
        resp.body = json.dumps({"login": "logged in successfully", "token": token})


class Logout:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        auth = req.get_header("Authorization").split(" ")
        token = auth[1]
        query = "select * from users"
        cur = mysql_action(query, "login")
        for user in cur:
            if token == user[3]:
                query = "update users set token = 'hhasfjkafkasjf41424' where id = {}".format(
                    user[0]
                )
                mysql_action(query, "logout")
        resp.body = json.dumps({"logout": "logged out successfully"})


def login(req, resp):
    auth = req.get_header("Authorization").split(" ")
    token = auth[1]
    query = "select * from users;"
    cur = mysql_action(query, "Authorization")
    for user in cur:
        user_token = user[3]
        token_time = user[4]
        if (user_token == token) and int(token_time) + 10000 > int(time.time()):
            token_time = time.time()
            query = "update users set token_time = {} where id = {} ;".format(
                token_time, user[0]
            )
            mysql_action(query, "Authorization")
            break
    else:
        raise falcon.HTTPUnauthorized(
            title="Login required", description="please do login"
        )
