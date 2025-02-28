---
title: Quick search with HTMX
summary: Add a quick search feature without page reload with HTMX
date: 2023-06-11
badge: code
image:
---

# Search with HTMX

## Whats is HTMX

Generated with chatGPT
> HTMX is a lightweight JavaScript library that allows for seamless and efficient communication between the server and the browser, enabling dynamic updates to web pages without the need for traditional page reloads.

In my words
> It is TailwindCSS for Javascript: keep all your code directly in your html file :)

## Implement a quick search

The steps to create your quick search feature are the following:

1. Add your `text input` in your HTML with HTMX attributes
2. Implement the view to handle the search request and perform the search action
3. Add your view in the `urls.py`

### 1. Create the text input attribute

```html
<input type="text"
       name="search"
       hx-post="{% url 'book_search' %}"
       hx-target = "#id_books"
       hx-trigger = "keyup changed delay:ms"
       placeholder="Search for books"
       class="input input-bordered w-full max-w-xs">
```

* `type="text"` In is a text input
* `name="search"` search is the name of the value that will be pass to the POST query
* `hx-post="{% url 'book_search' %}"` URL that will handle the POST query
* `hx-target = "#id_books"` Refer to the id of another element in the DOM that will be updated
* `hx-trigger = "keyup changed delay:ms"` The request is executed when the user type in the input, every 0.5s to handle quick key typing

### 2. Create the view to handle the request

```python
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
        'books': results.to_dict('records')
    }

    return render(request, 'blogApp/partials/books_partials.html', context)
```

### 3. Update `urls.py`

```python
htmx_urlpatterns = [
    path('book_search/', blogApp.views.book_search, name='book_search'),
]

urlpatterns += htmx_urlpatterns
```