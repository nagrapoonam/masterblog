from flask import Flask, render_template, request, redirect, url_for, flash
import json
import uuid
import secrets

app = Flask(__name__)
app.debug = True
app.secret_key = secrets.token_hex(16)
DATA_FILE = 'data.json'

def load_blog_posts():
    with open(DATA_FILE) as json_file:
        return json.load(json_file)

def save_blog_posts(blog_posts):
    with open(DATA_FILE, 'w') as json_file:
        json.dump(blog_posts, json_file)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
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

@app.route('/delete/<string:post_id>', methods=['GET', 'POST'])
def delete(post_id):
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


@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()

    post = next((post for post in blog_posts if str(post["id"]) == post_id), None)
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

@app.route('/like/<id>')
def like(id):
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
    app.run()

