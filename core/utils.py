import glob
import frontmatter
from operator import itemgetter
from datetime import date
import pandas as pd

def get_blogposts():
    all_posts = glob.glob("core/posts/**/*.md")
    posts = list()
    for filename in all_posts:
        post = frontmatter.load(filename)
        post_dict = {
            'title': post['title'],
            'summary': post['summary'],
            'date': post['date'],
            'badge': post['badge'],
            'image': post['image'],
            'content': post.content,
            'postname': filename.replace('\\', '/').split('/')[-1:][0]
        }
        if post['date'] <= date.today():
            posts.append(post_dict)
    return sorted(posts, key=itemgetter('date'), reverse=True)

def get_books():
    books_data = pd.read_csv('core/goodreads_library_export.csv')
    books_data = books_data.rename(columns=str.lower)
    books_data = books_data.rename(
        columns={
            "my rating": "my_rating",
            "average rating": "gr_rating"
        })
    books_data["date_read"] = pd.to_datetime(books_data["date read"], format='%Y/%m/%d')
    books_data = books_data[books_data["date_read"] >= "2020-01-01"]
    books_data["isbn"] = books_data["isbn"].str.replace('=', '')
    books_data["isbn"] = books_data["isbn"].str.replace('"', '')
    books_data = books_data[["title", "author", "date_read", "my_rating", "gr_rating", "isbn"]]
    books_data = books_data.sort_values("date_read", ascending=False)
    books_data["has_cover"] = books_data.isbn.apply(
        lambda x: len(glob.glob(f"core/static/images/covers/{x}-cover.jpg")) == 1)
    books_data["cover"] = books_data.isbn.apply(lambda x: f"images/covers/{x}-cover.jpg")
    books_data["cover"] = books_data.apply(lambda x: None if not x.has_cover else x.cover, axis=1)

    return books_data
