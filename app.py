from flask import Flask, request, render_template, redirect, url_for, make_response
import base64

app = Flask(__name__)

# Hardcoded credentials — intentionally simple for the CTF
USERS = {
    "player": "password123"
}

FLAG = "cusectf{enc0d1ng_1s_n0t_encryp710n}"


def get_role():
    """Decode the role cookie. Returns None if missing or invalid."""
    raw = request.cookies.get("role")
    if not raw:
        return None
    try:
        return base64.b64decode(raw.encode()).decode()
    except Exception:
        return None


@app.route("/")
def index():
    role = get_role()
    if role:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in USERS and USERS[username] == password:
            resp = make_response(redirect(url_for("dashboard")))
            # Vulnerable on purpose: role is just base64-encoded, not signed
            encoded_role = base64.b64encode(b"user").decode()
            resp.set_cookie("role", encoded_role)
            return resp
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    role = get_role()
    if not role:
        return redirect(url_for("login"))

    if role == "admin":
        return render_template("dashboard.html", role=role, flag=FLAG)
    else:
        return render_template("dashboard.html", role=role, flag=None)


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("role")
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
