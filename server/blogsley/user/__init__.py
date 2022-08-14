from enum import unique
from hashlib import md5

from tortoise.models import Model
from tortoise import fields

from blogsley.security import generate_password_hash, check_password_hash
'''
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''
class User(Model):
    class PydanticMeta:
        exclude = ["password_salt", "password_hash"]
        #computed = ["typename"]

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    firstName = fields.CharField(max_length=32)
    lastName = fields.CharField(max_length=32)
    email = fields.CharField(max_length=120, index=True, unique=True)
    password_salt = fields.BinaryField() #32
    password_hash = fields.BinaryField() #32
    role = fields.CharField(max_length=32)
    aboutMe = fields.CharField(max_length=140)

    posts: fields.ReverseRelation["Post"]

    def __repr__(self):
        return '<User {}>'.format(self.username)

    #def type_name():
    #    return "User"

    @property
    def full_name(self):
        return self.firstName + ' ' + self.lastName
    
    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        salt, key = generate_password_hash(password)
        self.password_salt = salt
        self.password_hash = key

    def check_password(self, password):
        return check_password_hash(password, self.password_salt, self.password_hash)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
