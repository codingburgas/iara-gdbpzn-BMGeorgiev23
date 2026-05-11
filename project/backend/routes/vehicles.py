from flask import Blueprint, jsonify
from data import VEHICLES

vehicles_bp = Blueprint("vehicles", __name__)


@vehicles_bp.route("/", methods=["GET"])
def get_vehicles():
    return jsonify(VEHICLES)


@vehicles_bp.route("/<vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    v = next((v for v in VEHICLES if v["id"] == vehicle_id), None)
    if not v:
        return jsonify({"error": "Not found"}), 404
    return jsonify(v)
