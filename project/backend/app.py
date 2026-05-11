from flask import Flask
from flask_cors import CORS
from routes.incidents import incidents_bp
from routes.teams import teams_bp
from routes.vehicles import vehicles_bp
from routes.schedule import schedule_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(incidents_bp, url_prefix="/api/incidents")
app.register_blueprint(teams_bp,     url_prefix="/api/teams")
app.register_blueprint(vehicles_bp,  url_prefix="/api/vehicles")
app.register_blueprint(schedule_bp,  url_prefix="/api/schedule")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
