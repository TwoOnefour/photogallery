from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)
import os
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Maximum file size: 16MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Dummy user model
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


# In-memory user store
users = {"user1": User(id=1, username="user1"), "user2": User(id=2, username="user2")}


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here you should add logic to verify username and password
        # For demonstration, we assume any password is correct
        if username in users:
            login_user(users[username])
            flash("Logged in successfully.")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle signup logic here
        pass
    return render_template("signup.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("index"))


@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Image successfully uploaded")
            return redirect(url_for("manage"))
    images = os.listdir(app.config["UPLOAD_FOLDER"])
    image_urls = [url_for("static", filename="uploads/" + image) for image in images]
    return render_template("manage.html", images=image_urls)


@app.route("/explore")
def explore():
    return render_template("explore.html")


@app.route("/random_images")
def random_images():
    image_files = os.listdir(app.config["UPLOAD_FOLDER"])
    random_images = random.sample(image_files, min(len(image_files), 10))
    image_urls = [
        url_for("static", filename="uploads/" + image) for image in random_images
    ]
    return jsonify(images=[{"url": url} for url in image_urls])


if __name__ == "__main__":
    app.run(debug=True)
