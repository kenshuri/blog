import glob

import frontmatter
from django.shortcuts import render, redirect

import os
import random

from core.utils import get_blogposts, get_books


# Create your views here.
def index(request):
    cover = '/static/images/welcome/webp/' + random.choice(os.listdir('core/static/images/welcome/webp/'))
    context = {
        'cover': cover
    }
    return render(request, 'core/index.html', context)

def posts(request):
    posts = get_blogposts()
    context = {
        'posts': posts
    }
    return render(request, 'core/posts.html', context)


def post_search(request):
    search_query = request.POST.get('search')
    if search_query:
        posts_data = get_blogposts()
        print(type(posts_data))
        for post in posts_data:
            print(post['title'])
        # Perform the search logic using a case-insensitive OR query
        results = list(filter(lambda post: search_query.lower() in post['title'].lower()
                                           or search_query.lower() in post['summary'].lower()
                                           or search_query.lower() in post['badge'].lower(), posts_data))
        for post in results:
            print(post['title'])
    else:
        # If no query is provided, return all books
        posts_data = get_blogposts()
        results = posts_data

    context = {
        'query': search_query,
        'posts': results
    }

    return render(request, 'core/partials/posts_partials.html', context)


def view_post(request, postname):
    try:
        postpath = glob.glob(f'core/posts/**/{postname}')[0]
        post = frontmatter.load(postpath)
        context = {
            'title': post['title'],
            'date': post['date'],
            'post_md': post.content,
        }
        return render(request, 'core/post.html', context)
    except FileNotFoundError:
        return render(request, 'core/missing_post.html')


def books(request):
    books_data = get_books()
    context = {
        'books': books_data.to_dict('records')
    }
    return render(request, 'core/books.html', context)


def book_search(request):
    search_query = request.POST.get('search')
    if search_query:
        books_data = get_books()
        # Perform the search logic using a case-insensitive OR query
        results = books_data[books_data['title'].str.contains(search_query, case=False) | books_data['author'].str.contains(search_query, case=False)]
    else:
        # If no query is provided, return all books
        books_data = get_books()
        results = books_data

    context = {
        'query': search_query,
        'books': results.to_dict('records')
    }

    return render(request, 'core/partials/books_partials.html', context)


def book_filter(request, stars):
    if stars in [1,2,3,4,5]:
        books_data = get_books()
        books_data = books_data[books_data["my_rating"] == stars]
        context = {
            'books': books_data.to_dict('records')
        }
        return render(request, 'core/partials/books_partials.html', context)
    else:
        return redirect('books')


def about(request):
    return render(request, 'core/about.html')