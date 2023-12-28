from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g,
    current_app,
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS
import os
from main.model.nb_cluster import cluster_review
from main.model.nb_kebersihan import predict_review_kebersihan
from main.model.nb_linen import predict_review_linen
from main.model.nb_service import predict_review_service
import pandas as pd
from werkzeug.utils import secure_filename

load_dotenv()

# app initialization and configiguration
app = Flask(__name__)
CORS(app)

app.config.from_mapping(
    SECRET_KEY=os.getenv("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI"),
    UPLOAD_FOLDER="uploads",
    ALLOWED_EXTENSIONS={"csv"},
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB limit
)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


with app.app_context():
    db.create_all()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


# Middleware to load the current user into the global context


@app.before_request
def load_user():
    if "user_id" in session:
        g.user = User.query.get(session["user_id"])
    else:
        g.user = None


# controllers
@app.route("/")
def dashboard():
    return render_template("dashboard/multi.html")


@app.route("/single")
def single():
    return render_template("dashboard/single.html")


# AUTH
@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        # Validate passwords
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create a new user
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully", "success")
        return redirect(url_for("login"))

    return render_template("auth/register.html")


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Query the user by email
        user = User.query.filter_by(email=email).first()

        # Validate user and password
        if user and bcrypt.check_password_hash(user.password, password):
            flash("Login successful", "success")

            # Set the user_id in the session
            session["user_id"] = user.id

            return redirect(url_for("dashboard"))
        else:
            flash("Login failed. Check your email and password", "danger")

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for("login"))


# Predict
@app.route("/predict-csv", methods=["POST"])
def predict():
    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Read CSV file into a DataFrame
            data = pd.read_csv(file_path)

            # cluster the file
            result_kebersihan, result_linen, result_service = cluster_review(
                data["review"]
            )

            # Predict using the provided function
            kebersihan_df = predict_review_kebersihan(result_kebersihan)
            service_df = predict_review_service(result_service)
            linen_df = predict_review_linen(result_linen)

            df_cluster = pd.concat([kebersihan_df, linen_df, service_df])

            samples_per_aspek = (
                df_cluster.groupby("aspek")
                .apply(lambda x: x.sample(5))
                .reset_index(drop=True)
            )

            labels_cluster = df_cluster["aspek"].value_counts().index.tolist()
            counts_cluster = df_cluster["aspek"].value_counts().tolist()

            # Extract labels and their counts for each aspect
            labels_kebersihan = kebersihan_df["label"].value_counts().index.tolist()
            counts_kebersihan = kebersihan_df["label"].value_counts().tolist()

            labels_service = service_df["label"].value_counts().index.tolist()
            counts_service = service_df["label"].value_counts().tolist()

            labels_linen = linen_df["label"].value_counts().index.tolist()
            counts_linen = linen_df["label"].value_counts().tolist()

            return render_template(
                "predict/result_csv.html",
                labels_kebersihan=labels_kebersihan,
                counts_kebersihan=counts_kebersihan,
                labels_service=labels_service,
                counts_service=counts_service,
                labels_linen=labels_linen,
                counts_linen=counts_linen,
                labels_cluster=labels_cluster,
                counts_cluster=counts_cluster,
                samples_per_aspek=samples_per_aspek,
            )

    return render_template("dashboard/multi.html")


@app.route("/predict-single", methods=["POST"])
def predict_single():
    if request.method == "POST":
        print("single")
        return render_template("predict/result_single.html")

    return render_template("dashboard/single.html")
