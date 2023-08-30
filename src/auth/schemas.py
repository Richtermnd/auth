from pydantic import BaseModel, constr


# TODO: Add password validation.
# Regex for password from StackOverflow doesn't work, so now it's not my problem, yeah.
class CreateUser(BaseModel):
    username: constr(min_length=5, to_lower=True, pattern='[a-zA-Z0-9_.]+$')
    password: constr(min_length=8)
    repeat_password: constr(min_length=8)


class LoginUser(BaseModel):
    username: str
    password: str
    

class User(BaseModel):
    id: int
    username: str

    model_config = {
        'from_attributes': True
    }


class Token(BaseModel):
    access_token: str
    type: str = 'Bearer'
    