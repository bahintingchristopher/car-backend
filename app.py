from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
for werkzeug.utils import secure_filename #new import
import json, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend (GitHub Pages) to fetch data

DATA_FILE = "cars.json"

# Serve uploaded images
@app.route("/static/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("static/uploads", filename)

# Load car data
def load_cars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
    
# File upload configuration
UPLOADER_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOADER_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("admin/add", methods=['POST'])
def add_car_with_image():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Now save the car data
        cars = load_cars()
        new_car = {
            "name": request.form["name"],
            "image": filename,  # Save only the filename
            "price": request.form["price"]
        }
        cars.append(new_car)
        save_cars(cars)
        return redirect(url_for("admin"))
    




# Save car data
def save_cars(cars):
    with open(DATA_FILE, "w") as f:
        json.dump(cars, f, indent=4)

# API endpoint for frontend
@app.route("/cars", methods=["GET"])
def get_cars():
    cars = load_cars()     
    return jsonify(cars)

# Admin Panel
@app.route("/admin")
def admin():
    cars = load_cars()
    return render_template("admin.html", cars=cars)

@app.route("/admin/add", methods=["POST"])
def add_car():
    cars = load_cars()
    new_car = {
        "name": request.form["name"],
        "image": request.form["image"],  # filename like "civic.jpg"
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

@app.route("/")
def home():
     return redirect(url_for("get_cars"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
