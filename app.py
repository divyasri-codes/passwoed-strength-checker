
from flask import Flask, render_template, request
import re

app = Flask(__name__)


def check_password(password):
    score = 0
    suggestions = []

    checks = {
        "At least 8 characters": len(password) >= 8,
        "At least 12 characters (recommended)": len(password) >= 12,
        "Contains uppercase letters": bool(re.search(r"[A-Z]", password)),
        "Contains lowercase letters": bool(re.search(r"[a-z]", password)),
        "Contains numbers": bool(re.search(r"[0-9]", password)),
        "Contains special characters": bool(
            re.search(r"[^A-Za-z0-9]", password)
        ),
    }

    for description, passed in checks.items():
        if passed:
            score += 1
        else:
            suggestions.append(description)

    if not password:
        strength = "Not evaluated"
        level = 0
    elif len(password) < 8:
        strength = "Weak"
        level = 1
    elif score <= 3:
        strength = "Medium"
        level = 2
    elif score <= 5:
        strength = "Strong"
        level = 3
    else:
        strength = "Very Strong"
        level = 4

    return strength, level, checks, suggestions


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    level = 0
    checks = {}
    suggestions = []

    if request.method == "POST":
        password = request.form.get("password", "")
        result, level, checks, suggestions = check_password(password)

    return render_template(
        "index.html",
        result=result,
        level=level,
        checks=checks,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)
