"""
Blog Application Example
This is a simple blog application built with our custom web framework.
"""

import os
import sys
import json
from datetime import datetime

# Add the framework to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from framework import app, route, HTTPResponse
from middleware import LoggingMiddleware, JSONMiddleware, SessionMiddleware
from plugins.static_files import setup_static_files
from plugins.cors import setup_cors
from utils.helpers import json_response, redirect, hash_password, verify_password
from sessions import session_manager


# Simple in-memory data store (in a real app, you'd use a database)
posts = [
    {
        "id": 1,
        "title": "Welcome to My Blog",
        "content": "This is the first post on my blog. Welcome!",
        "author": "Admin",
        "date": "2023-01-01T12:00:00Z"
    },
    {
        "id": 2,
        "title": "Learning Python Web Development",
        "content": "Today I'm learning how to build web applications with Python.",
        "author": "Admin",
        "date": "2023-01-02T14:30:00Z"
    }
]

users = [
    {
        "id": 1,
        "username": "admin",
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
        "salt": "salt",
        "is_admin": True
    }
]

# Setup middleware
app.add_middleware(LoggingMiddleware())
app.add_middleware(JSONMiddleware())
app.add_middleware(SessionMiddleware())

# Setup plugins
setup_static_files(app)
setup_cors(app)

# Routes
@route("/")
def index(request):
    """Home page showing all blog posts."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Blog</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .post { border-bottom: 1px solid #ccc; margin-bottom: 20px; padding-bottom: 20px; }
            .post-title { color: #333; }
            .post-meta { color: #666; font-size: 0.9em; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 10px; }
        </style>
    </head>
    <body>
        <h1>My Blog</h1>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/posts/new">New Post</a>
            <a href="/login">Login</a>
        </div>
    """
    
    for post in posts:
        html += f"""
        <div class="post">
            <h2 class="post-title"><a href="/posts/{post['id']}">{post['title']}</a></h2>
            <div class="post-meta">By {post['author']} on {post['date']}</div>
            <p>{post['content'][:200]}{'...' if len(post['content']) > 200 else ''}</p>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html


@route("/posts/{post_id}")
def show_post(request):
    """Show a specific blog post."""
    post_id = int(request.params['post_id'])
    
    # Find the post
    post = None
    for p in posts:
        if p['id'] == post_id:
            post = p
            break
    
    if not post:
        return HTTPResponse("Post not found", status_code=404)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{post['title']} - My Blog</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .post-title {{ color: #333; }}
            .post-meta {{ color: #666; font-size: 0.9em; }}
            .nav {{ margin-bottom: 20px; }}
            .nav a {{ margin-right: 10px; }}
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/posts/new">New Post</a>
            <a href="/login">Login</a>
        </div>
        <h1 class="post-title">{post['title']}</h1>
        <div class="post-meta">By {post['author']} on {post['date']}</div>
        <div>{post['content']}</div>
    </body>
    </html>
    """
    
    return html


@route("/posts/new", methods=["GET"])
def new_post_form(request):
    """Show form to create a new blog post."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>New Post - My Blog</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, textarea { width: 100%; padding: 8px; }
            textarea { height: 200px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 10px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/posts/new">New Post</a>
            <a href="/login">Login</a>
        </div>
        <h1>Create New Post</h1>
        <form method="POST" action="/posts">
            <div class="form-group">
                <label for="title">Title:</label>
                <input type="text" id="title" name="title" required>
            </div>
            <div class="form-group">
                <label for="content">Content:</label>
                <textarea id="content" name="content" required></textarea>
            </div>
            <div class="form-group">
                <label for="author">Author:</label>
                <input type="text" id="author" name="author" required>
            </div>
            <button type="submit">Create Post</button>
        </form>
    </body>
    </html>
    """
    
    return html


@route("/posts", methods=["POST"])
def create_post(request):
    """Create a new blog post."""
    # In a real app, you'd want to validate and sanitize input
    title = request.body.get('title', '')
    content = request.body.get('content', '')
    author = request.body.get('author', 'Anonymous')
    
    # Create new post
    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "content": content,
        "author": author,
        "date": datetime.utcnow().isoformat() + "Z"
    }
    
    posts.append(new_post)
    
    # Redirect to the new post
    return redirect(f"/posts/{new_post['id']}")


@route("/api/posts")
def api_posts(request):
    """API endpoint to get all posts."""
    return json_response({"posts": posts})


@route("/api/posts/{post_id}")
def api_post(request):
    """API endpoint to get a specific post."""
    post_id = int(request.params['post_id'])
    
    # Find the post
    post = None
    for p in posts:
        if p['id'] == post_id:
            post = p
            break
    
    if not post:
        return json_response({"error": "Post not found"}, status_code=404)
    
    return json_response({"post": post})


@route("/login", methods=["GET"])
def login_form(request):
    """Show login form."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - My Blog</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input { width: 100%; padding: 8px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 10px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/">Home</a>
            <a href="/posts/new">New Post</a>
            <a href="/login">Login</a>
        </div>
        <h1>Login</h1>
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """
    
    return html


@route("/login", methods=["POST"])
def login(request):
    """Handle login."""
    username = request.body.get('username', '')
    password = request.body.get('password', '')
    
    # Find user
    user = None
    for u in users:
        if u['username'] == username:
            user = u
            break
    
    if not user:
        return HTTPResponse("Invalid username or password", status_code=401)
    
    # Verify password
    if not verify_password(password, user['password_hash'], user['salt']):
        return HTTPResponse("Invalid username or password", status_code=401)
    
    # Create session
    if not request.session:
        request.session = session_manager.create_session()
    
    request.session.set('user_id', user['id'])
    request.session.set('username', user['username'])
    request.session.set('is_admin', user['is_admin'])
    
    # Redirect to home
    return redirect("/")


@route("/logout")
def logout(request):
    """Handle logout."""
    if request.session:
        session_manager.destroy_session(request.session.session_id)
    
    return redirect("/")


# Error handlers
@app.errorhandler(404)
def not_found(request):
    """Handle 404 errors."""
    return HTTPResponse("<h1>Page Not Found</h1><p>The page you are looking for does not exist.</p>", status_code=404)


@app.errorhandler(500)
def internal_error(request):
    """Handle 500 errors."""
    return HTTPResponse("<h1>Internal Server Error</h1><p>Something went wrong on our end.</p>", status_code=500)


if __name__ == "__main__":
    print("Starting blog application...")
    print("Visit http://localhost:8000 in your browser")
    app.run(host="localhost", port=8000)