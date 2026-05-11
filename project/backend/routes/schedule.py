from flask import Blueprint, jsonify
from data import SCHEDULE

schedule_bp = Blueprint("schedule", __name__)


@schedule_bp.route("/", methods=["GET"])
def get_schedule():
    on_duty = [s for s in SCHEDULE if s["shift"] != "—" and not s["sick"]]
    on_leave = [s for s in SCHEDULE if s["leave"]]
    sick     = [s for s in SCHEDULE if s["sick"]]

    return jsonify({
        "entries":   SCHEDULE,
        "on_duty":   len(on_duty),
        "on_leave":  len(on_leave),
        "sick":      len(sick),
    })
