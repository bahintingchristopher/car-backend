from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend (GitHub Pages) to fetch data

DATA_FILE = "cars.json"

# Load car data
def load_cars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save car data
def save_cars(cars):
    with open(DATA_FILE, "w") as f:
        json.dump(cars, f, indent=4)

# ✅ API endpoint for frontend
@app.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(load_cars())

# ✅ Admin Panel
@app.route("/admin")
def admin():
    cars = load_cars()
    return render_template("admin.html", cars=cars)

@app.route("/admin/add", methods=["POST"])
def add_car():
    cars = load_cars()
    new_car = {
        "name": request.form["name"],
        "image": request.form["image"],   # filename like "civic.jpg"
        "price": request.form["price"]
    }
    cars.append(new_car)
    save_cars(cars)
    return redirect(url_for("admin"))

@app.route("/admin/edit/<int:car_id>", methods=["POST"])
def edit_car(car_id):
    cars = load_cars()
    if 0 <= car_id < len(cars):
        cars[car_id]["name"] = request.form["name"]
        cars[car_id]["image"] = request.form["image"]
        cars[car_id]["price"] = request.form["price"]
        save_cars(cars)
    return redirect(url_for("admin"))

@app.route("/admin/delete/<int:car_id>")
def delete_car(car_id):
    cars = load_cars()
    if 0 <= car_id < len(cars):
        cars.pop(car_id)
        save_cars(cars)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    # Use Render's port or default to 10000 for local testing
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
