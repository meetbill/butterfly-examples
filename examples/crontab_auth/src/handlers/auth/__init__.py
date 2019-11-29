# coding=utf8
from xlib.httpgateway import Request
from xlib import retstat
from model import User
from xlib import middleware
from xlib.db import shortcuts
from xlib import auth

__info__ = "meetbill"
__version__ = "1.0.1"


@middleware.db_close
def login(req,username,password):
    isinstance(req,Request)
    result = {}
    result["success"] = False
    result["message"] = ""
    result["data"] = {}
    try:
        user = User().select().where(User.username == username).get()
    except Exception as e:
        result["message"] = str(e)
        return retstat.HTTP_OK, result, [(__info__, __version__)]
    if  shortcuts.model_to_dict(user)["password"] == password:
        token = auth.gen_token(username)
        token = token.decode("utf-8")
        data = {}
        result["success"] = True
        data["token"] = token
        data["username"] =  username
        data["permissions"] = ""
        result["data"] = data
        return retstat.HTTP_OK, result, [(__info__, __version__)]
    else:
        result["message"] = "Password not match"
        return retstat.HTTP_OK, result, [(__info__, __version__)]
