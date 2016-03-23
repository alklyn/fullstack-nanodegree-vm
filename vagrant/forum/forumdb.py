#
# Database access functions for the web forum.
#

import time
import psycopg2
import psycopg2.extras




## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = '''
    select content, time
    from posts
    order by time
    '''
    cur.execute(query)
    posts = cur.fetchall()
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    DB.close()
    print(posts)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    query = '''
    insert
    into posts(content) values(%s)
    '''
    query = query.format(new_content = content, t_stamp = t)
    cur.execute(query, (content,))
    DB.commit()
    DB.close()
