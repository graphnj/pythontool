
from fastapi import Depends
from sqlalchemy.orm import Session
from server.utils.serverUtils import BaseResponse


def hello():
    res = {'hh':'sss'}
    return BaseResponse(code = 200,data = res)