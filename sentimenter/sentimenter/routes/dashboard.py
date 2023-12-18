from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

bp = Blueprint("documents", __name__, url_prefix="/")


@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "GET":
        return render_template("dashboard/index.html")


@bp.route('/batch', methods=["GET"])
def batch():
    if request.method == "GET":
        return render_template("dashboard/batch.html")