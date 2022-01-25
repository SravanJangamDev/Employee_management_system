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
        print("Login here")
        for user in cur:
            actual_password = user[2].encode("utf-8")
            salt = user[5].encode("utf-8")
            user_hash = bcrypt.hashpw(entered_password, salt)
            actual_hash = bcrypt.hashpw(actual_password, salt)
            valid_pwd = bcrypt.checkpw(user_hash, actual_hash)
            if user[1] == username and valid_pwd:
                jwt_secret_key = uuid.uuid4().hex
                token_key = "user:{}".format(user[0])
                redis_cli.set(token_key, jwt_secret_key)
                redis_cli.expire(token_key,100)
                #payload = {"user-id": user[0], "username": username}
                # token = jwt.encode(payload, jwt_secret_key, "HS256").decode("utf-8")
                #token = jwt_secret_key
                #token_time = time.time()
                #query = "update users set token = '{}' , token_time = {} where id = {} ".format(
                 #   token, token_time, user[0]
                #)
                #mysql_action(query, "login")
                print(jwt_secret_key)
                resp.set_header("token", jwt_secret_key)
                resp.body = json.dumps({"login": "logged in successfully", "token" : jwt_secret_key, "user_id" : user[0]})
                break
        else:
            raise falcon.HTTPUnauthorized(
                title="Login failed", description="Invalid username or password"
            )
        print("logged in successfully")


class Logout:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        auth = req.get_header("Authorization").split(" ")
        token = auth[1]
        user_id = req.get_header("user")
        token_key = "user:{}".format(user_id)
        token = redis_cli.get(token_key)
        if token is None:
        	raise falcon.HTTPUnauthorized(title="Login required", description="please do login")
        else:
        	if(token != token_entered):
        		raise falcon.HTTPUnauthorized(title="Login required", description="please do login")
        	redis_cli.expire(token_key, 0)

        resp.body = json.dumps({"logout": "logged out successfully"})


def login(req, resp):
    auth = req.get_header("Authorization").split(" ")
    token_entered = auth[1]
    user_id = req.get_header("user")
    token_key = "user:{}".format(user_id)
    token = redis_cli.get(token_key)
    if token is None:
    	raise falcon.HTTPUnauthorized(title="Login required", description="please do login")
    else:
    	print(token, token_entered)
    	token = token.decode("utf-8")
    	if(token != token_entered):
    		raise falcon.HTTPUnauthorized(title="Login required", description="please do login")
    	redis_cli.expire(token_key, 100)

