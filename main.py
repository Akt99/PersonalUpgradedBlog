from flask import Flask, render_template, request
import requests as req
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL=os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")

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
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post=None
    for blog_post in posts:
        if blog_post["id"]== index:
            requested_post=blog_post
    return render_template("post.html",post=requested_post)
def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message} "
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(EMAIL, email , email_message)

if __name__ == "__main__":
    app.run(debug=True, port=5002)