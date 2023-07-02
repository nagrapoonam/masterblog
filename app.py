# By importing these modules,utilizing their functions and features
# to work with JSON data,generate secure random values, and create unique identifiers.
import json
import secrets
import uuid

# By importing these modules and functions,utilizing Flask features and functionalities,
# for rendering templates, handling requests, performing redirects, generating URLs, and displaying flash messages.
from flask import Flask, render_template, request, redirect, url_for, flash

# Initializing a Flask application instance,
# enables debug mode, sets a secret key,
# and assigns a filename to a variable for referencing a JSON data file.
app = Flask(__name__)
app.debug = True
app.secret_key = secrets.token_hex(16)
DATA_FILE = 'data.json'


def load_blog_posts():
    """This function loads blog posts from a JSON file
    by reading its contents with open function."""
    with open(DATA_FILE) as json_file:
        return json.load(json_file)


def save_blog_posts(blog_posts):
    """This function takes a data containing blog posts,
    opens a JSON file, serializes the data into JSON format,
    and writes it to the file specified by DATA_FILE."""
    with open(DATA_FILE, 'w') as json_file:
        json.dump(blog_posts, json_file)


# handler for the root URL. loading posts and render index.hmtl
@app.route('/')
def index():
    """function loads blog posts
    and renders the index.html
    template with the blog posts data"""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


# allows both GET and POST requests to be made to the "/add" URL
@app.route('/add', methods=['GET', 'POST'])
def add():
    """function handles both GET and POST requests.
    When a POST request is made, it processes the submitted form data,
    creates new blog post, appends it to the existing posts, saves the updated posts to a JSON file,
    provides a success flash message, and redirects the user to the "index" page.
    When a GET request is made, it renders the "add.html" template."""
    blog_posts = load_blog_posts()
    if request.method == 'POST':
        # Handle the POST request to add a new blog post
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Generate a unique ID for the new blog post
        unique_id = str(uuid.uuid4())

        new_post = {
            "id": unique_id,
            "author": author,
            "title": title,
            "content": content
        }

        # Append the new post to the existing blog posts
        blog_posts.append(new_post)

        # Save the updated blog posts back to the JSON file
        save_blog_posts(blog_posts)

        flash('Blog post added successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('add.html')


# allows both GET and POST requests to be made to the "/delete" URL
@app.route('/delete/<string:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """function loads the blog posts, removes the post with the specified ID from the list,
    saves the updated list to a JSON file, provides a success flash message,
    and redirects the user to the "index" page after the deletion is complete"""
    blog_posts = load_blog_posts()

    # Find the post with the specified ID and remove it from the blog posts
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    # Save the updated blog posts back to the JSON file
    save_blog_posts(blog_posts)

    flash('Blog post deleted successfully!', 'success')

    return redirect(url_for('index'))


# allows both GET and POST requests to be made to the "/update" URL
@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """ function loads the blog posts,
    finds the post with the specified ID,
    updates its details if the request method is POST,
    saves the updated list to a JSON file,
    provides a success flash message,
    and redirects the user to the "index" page after the update is complete.
    If the request method is GET, it renders the "update.html" template with the specific post data.
    """
    blog_posts = load_blog_posts()

    post = next((post for post in blog_posts if str(post["id"]) == post_id),
                None)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Update the details of the blog post
        post["author"] = author
        post["title"] = title
        post["content"] = content

        # Save the updated blog posts back to the JSON file
        save_blog_posts(blog_posts)

        flash('Blog post updated successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# this route handle requests to the "/like/<id>" URL path
@app.route('/like/<id>')
def like(id):
    """function fetches the blog posts,
    finds the post with the given ID,
    increments or initializes the 'likes' count for that post,
    saves the updated list to the JSON file,
    provides a success flash message,
    and redirects the user to the "index" page.
    """
    # Fetch the blog posts from the JSON file
    blog_posts = load_blog_posts()

    # Find the post with the given id
    for post in blog_posts:
        if str(post['id']) == id:
            # Check if 'likes' key exists in the post dictionary
            if 'likes' in post:
                # Increment the likes count
                post['likes'] += 1
            else:
                # Initialize 'likes' key if it doesn't exist
                post['likes'] = 1

            # Save the updated blog posts back to the JSON file
            save_blog_posts(blog_posts)

            flash('Post liked!', 'success')
            break

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
