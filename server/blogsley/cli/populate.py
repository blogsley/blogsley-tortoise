import asyncio

import click

from blogsley.db import init_db
from blogsley.security import generate_password_hash

from blogsley.user import User
from blogsley.post import Post

@click.command()
@click.pass_context
def populate(ctx):
    asyncio.run(_populate())

block = """
{
  "type": "Page",
  "id": "UcGgZlHKqLcUtZrhD1gmc",
  "_value": null,
  "html": "",
  "children": [
    {
      "type": "Title",
      "id": "7D51SWIHpZ_8jyAxtKFIr",
      "_value": "Bazinga!",
      "html": "<h1>Bazinga!</h1>",
      "children": []
    },
    {
      "type": "Paragraph",
      "id": "gA1RyeFDpcEEAfBdXhQvU",
      "_value": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
      "html": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
      "children": [],
      "content": {
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
              }
            ]
          }
        ]
      }
    },
    {
      "type": "Image",
      "id": "U1AJAk6v8pOqcchxSAZOH",
      "_value": null,
      "html": "",
      "children": [],
      "src": "statics/images/journal-on-desk.jpg",
      "width": 256,
      "height": 256
    },
    {
      "type": "Heading",
      "id": "2wWjwHazm8jVLLZAHnbvl",
      "_value": "Heading",
      "html": "<h2>Heading</h2>",
      "children": [],
      "content": {
        "type": "doc",
        "content": [
          {
            "type": "heading",
            "attrs": {
              "level": 2
            },
            "content": [
              {
                "type": "text",
                "text": "Heading"
              }
            ]
          }
        ]
      }
    },
    {
      "type": "Paragraph",
      "id": "BXVQVXVk5KJCh48gEubqp",
      "_value": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
      "html": "<p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>",
      "children": [],
      "content": {
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
              }
            ]
          }
        ]
      }
    },
    {
      "type": "Html",
      "id": "tTaKSi7UPbuywEajPrcZY",
      "_value": null,
      "html": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p><p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>",
      "children": [],
      "content": {
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
              }
            ]
          },
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
              }
            ]
          }
        ]
      }
    },
    {
      "type": "List",
      "id": "N6_UoyNfcEr24e581nsUP",
      "_value": [
        "Get Milk",
        "Get Bread",
        "Get Butter"
      ],
      "html": "<ul><li><p>Get Milk</p></li><li><p>Get Bread</p></li><li><p>Get Butter</p></li></ul>",
      "children": [],
      "content": {
        "type": "doc",
        "content": [
          {
            "type": "bullet_list",
            "content": [
              {
                "type": "list_item",
                "content": [
                  {
                    "type": "paragraph",
                    "content": [
                      {
                        "type": "text",
                        "text": "Get Milk"
                      }
                    ]
                  }
                ]
              },
              {
                "type": "list_item",
                "content": [
                  {
                    "type": "paragraph",
                    "content": [
                      {
                        "type": "text",
                        "text": "Get Bread"
                      }
                    ]
                  }
                ]
              },
              {
                "type": "list_item",
                "content": [
                  {
                    "type": "paragraph",
                    "content": [
                      {
                        "type": "text",
                        "text": "Get Butter"
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  ]
}
"""


async def _populate():
    await init_db()

    (salt, key) = generate_password_hash('blogsley')
    u = User(
        username="admin",
        firstName="The",
        lastName="Admin",
        email="admin@example.com",
        role="Admin",
        aboutMe="I am the Admin",
        password_salt=salt,
        password_hash=key,
    )
    await u.save()

    u = User(
        username="john",
        firstName="John",
        lastName="Doe",
        email="john@example.com",
        role="Editor",
        aboutMe="I am an Editor",
        password_salt=salt,
        password_hash=key,
    )
    await u.save()

    p = Post(
        title="Blogsley, Web Publishing Evolved",
        block=block,
        body="Blogsley is a CMS for the JAMstack",
        author=u,
    )
    await p.save()
    
    u = User(
        username="susan",
        firstName="Susan",
        lastName="Smith",
        email="susan@example.com",
        role="Author",
        aboutMe="I am an Author",
        password_salt=salt,
        password_hash=key,
    )
    await u.save()

    p = Post(
        title="Python is cool!",
        block=block,
        body="I love writing programs in Python",
        author=u,
    )
    await p.save()

    u = User(
        username="joe",
        firstName="Joe",
        lastName="Jackson",
        email="joe@example.com",
        role="Reader",
        aboutMe="I am a Reader",
        password_salt=salt,
        password_hash=key,
    )
    await u.save()

    users = await User.all()
    for u in users:
        print(u)

    posts = await Post.all().prefetch_related('author')
    
    for p in posts:
        print(p.id, p.author.username, p.body)
