from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

coop_bp = Blueprint("coop", __name__)

@coop_bp.route("/api/coop_updates/<int:coop_id>", methods=["PUT"])
def update_coop(coop_id):
    try:
        # Retrieve the update data from the request
        updates = request.json

        # Validate that there's at least one field to update
        if not updates:
            return jsonify({"error": "No fields provided for update"}), 400

        # Build the dynamic update query
        query_parts = []
        params = []
        if "PositionTitle" in updates:
            query_parts.append("PositionTitle = %s")
            params.append(updates["PositionTitle"])
        if "CompanyName" in updates:
            query_parts.append("CompanyName = %s")
            params.append(updates["CompanyName"])
        if "StartDate" in updates:
            query_parts.append("StartDate = %s")
            params.append(updates["StartDate"])
        if "EndDate" in updates:
            query_parts.append("EndDate = %s")
            params.append(updates["EndDate"])

        if not query_parts:
            return jsonify({"error": "No valid fields provided for update"}), 400

        # Construct and execute the query
        query = f"UPDATE Coops SET {', '.join(query_parts)} WHERE CoOpID = %s"
        params.append(coop_id)

        conn = mysql.connector.connect(user="root", password="password", database="startupconnect")
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))

        # Check if the record was updated
        if cursor.rowcount == 0:
            return jsonify({"error": f"No Co-op found with ID {coop_id}"}), 404

        conn.commit()
        return jsonify({"message": f"Co-op {coop_id} updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500