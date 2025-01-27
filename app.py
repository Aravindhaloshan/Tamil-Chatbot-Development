from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.route("/")
def index_get():
    return render_template("base.html")

@app.route("/about")
def about_get():
    return render_template("about.html")

@app.route("/events")
def events_get():
    return render_template("events.html")

@app.route("/course")
def course_get():
    return render_template("course.html")

@app.route("/contact")
def contact_get():
    return render_template("contact.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message) 

if __name__ == "__main__":
    app.run(debug=True)
