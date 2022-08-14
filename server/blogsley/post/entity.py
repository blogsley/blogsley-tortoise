from datetime import datetime
from slugify import slugify

from tortoise.models import Model
from tortoise import fields

from blogsley.config import db

class Post(Model):
    id = fields.IntField(pk=True)
    status = fields.CharField(max_length=16, default='draft')
    title = fields.CharField(max_length=256)
    slug = fields.CharField(max_length=256, null=True)
    block = fields.TextField()
    cover = fields.CharField(max_length=256, null=True)
    body = fields.TextField()
    timestamp = fields.DatetimeField(index=True, default=datetime.utcnow())
    author = fields.ForeignKeyField('models.User', related_name='posts')
    # tags

    def __init__(self, *args, **kwargs):
        
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))

        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        super(Post, self).__setattr__(key, value)
        if key == 'title':
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

'''
@event.listens_for(Post.body, 'set', retval=True)
def validate_body(target, value, oldvalue, initiator):
    return BeautifulSoup(value, 'html.parser').prettify()
'''