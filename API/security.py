from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'joe', 'password')
]

# users dict with username as key
username_table = { u.username : u for u in users}

# users dict with userid as key
userid_table ={u.id : u for u in users}

def authenticate(username, password):
    '''Validates if a username is present'''
    user = username_table.get(username, None)
    if user is not None and safe_str_cmp(password,user.password):
        #return user.id, user.username, user.password'
        return user

def identity(payload):
    '''Validates if a userid is present'''
    user_id = payload['identity']
    return userid_table.get(user_id, None)


#print(authenticate('joe', 'password'))
# print(identity({'identity': 1}))
