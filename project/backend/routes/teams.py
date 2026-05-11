from flask import Blueprint, jsonify
from data import TEAMS, STAFF

teams_bp = Blueprint("teams", __name__)


@teams_bp.route("/", methods=["GET"])
def get_teams():
    return jsonify(TEAMS)


@teams_bp.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = next((t for t in TEAMS if t["id"] == team_id), None)
    if not team:
        return jsonify({"error": "Not found"}), 404

    members = [s for s in STAFF if s["team"] == team["name"]]
    return jsonify({**team, "staff": members})
