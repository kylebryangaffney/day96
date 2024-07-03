from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

NASA_API_KEY = os.getenv("NASA_API_KEY")

rover_list = ["Curiosity", "Opportunity", "Spirit"]
camera_dict = {
    "Front Hazard Avoidance Camera": "FHAZ",
    "Rear Hazard Avoidance Camera": "RHAZ",
    "Navigation Camera": "NAVCAM",
    "Panoramic Camera": "PANCAM"
}

class RoverForm(FlaskForm):
    name = SelectField('Rover Name', choices=[(rover, rover) for rover in rover_list], validators=[DataRequired()])
    date = DateField('Date of Pictures', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.route("/", methods=['GET', 'POST'])
def home():
    form = RoverForm()
    if form.validate_on_submit():
        rover_name = form.name.data.lower()
        date = form.date.data.strftime('%Y-%m-%d')
        return redirect(url_for('results', rover_name=rover_name, date=date))
    
    return render_template("index.html", form=form)

@app.route("/results")
def results():
    rover_name = request.args.get('rover_name')
    date = request.args.get('date')

    response = requests.get(url=f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?earth_date={date}&api_key={NASA_API_KEY}")
    response.raise_for_status()
    query_data = response.json()

    panoramic_camera = []
    front_hazard_camera = []
    rear_hazard_camera = []

    # Iterate through each photo and categorize by camera type
    for photo in query_data["photos"]:
        camera_name = photo["camera"]["name"]
        img_src = photo["img_src"]
        
        if camera_name == "PANCAM":
            panoramic_camera.append(img_src)
        elif camera_name == "FHAZ":
            front_hazard_camera.append(img_src)
        elif camera_name == "RHAZ":
            rear_hazard_camera.append(img_src)

    return render_template('results.html', panoramic_camera=panoramic_camera, front_hazard_camera=front_hazard_camera, rear_hazard_camera=rear_hazard_camera)

if __name__ == '__main__':
    app.run(debug=True)

rover_list = ["Curiosity", "Opportunity", "Spirit"]
date = input("Date yyyy-mm-dd: ")
rover = input("Rover: ")
camera = {
    "Front Hazard Avoidance Camera": "FHAZ",
    "Rear Hazard Avoidance Camera": "RHAZ",
    "Navigation Camera": "NAVCAM"
}

response = requests.get(url=f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={NASA_API_KEY}")
print(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={NASA_API_KEY}")

response.raise_for_status()

query_data = response.json()

panoramic_camera = []
front_hazard_camera = []
rear_hazard_camera = []

# Iterate through each photo and categorize by camera type
for photo in query_data["photos"]:
    camera_name = photo["camera"]["name"]
    img_src = photo["img_src"]
    
    if camera_name == "PANCAM":
        panoramic_camera.append(img_src)
    elif camera_name == "FHAZ":
        front_hazard_camera.append(img_src)
    elif camera_name == "RHAZ":
        rear_hazard_camera.append(img_src)

# Print the lists
print("Panoramic Camera:", panoramic_camera)
print("Front Hazard Camera:", front_hazard_camera)
print("Rear Hazard Camera:", rear_hazard_camera)
