from flask import Flask, render_template
import requests as req
try:
    response = req.get("https://api.npoint.io/cf8f7c02bafac481bab0")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    response.raise_for_status()  # Check for HTTP errors
    posts = response.json()  # Attempt to parse the response as JSON
    print(f"Response JSON: {posts}")

except req.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    posts = []  # Default to empty posts
except req.exceptions.RequestException as err:
    print(f"Other error occurred: {err}")
    posts = []  # Default to empty posts
except ValueError as json_err:
    print(f"JSON decode error: {json_err}")
    posts = []  # Default to empty posts

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/post/<int:index>")
def show_post(index):
    requested_post=None
    for blog_post in posts:
        if blog_post["id"]== index:
            requested_post=blog_post
    return render_template("post.html",post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)