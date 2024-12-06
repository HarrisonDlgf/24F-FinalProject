from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

coop = Blueprint("coop", __name__)


# PUT: Update an existing co-op record
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
        conn.commit()

        return jsonify({"message": f"Co-op {coop_id} updated successfully"}), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# POST: Create a new co-op
@coop_bp.route("/api/coop_updates", methods=["POST"])
def create_coop():
    try:
        # Retrieve co-op details from the request
        data = request.json
        required_fields = ["PositionTitle", "CompanyName", "StartDate", "EndDate"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Insert the new co-op into the database
        query = """
            INSERT INTO Coops (PositionTitle, CompanyName, StartDate, EndDate)
            VALUES (%s, %s, %s, %s)
        """
        params = (data["PositionTitle"], data["CompanyName"], data["StartDate"], data["EndDate"])

        conn = mysql.connector.connect(user="root", password="password", database="startupconnect")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        return jsonify({"message": "Co-op created successfully", "CoOpID": cursor.lastrowid}), 201

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# DELETE: Delete a co-op by ID
@coop_bp.route("/api/coop_updates/<int:coop_id>", methods=["DELETE"])
def delete_coop(coop_id):
    try:
        # Delete the co-op from the database
        query = "DELETE FROM Coops WHERE CoOpID = %s"
        conn = mysql.connector.connect(user="root", password="password", database="startupconnect")
        cursor = conn.cursor()
        cursor.execute(query, (coop_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": f"No co-op found with ID {coop_id}"}), 404

        return jsonify({"message": f"Co-op {coop_id} deleted successfully"}), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# GET: Retrieve a co-op by ID
@coop_bp.route("/api/coop_updates/<int:coop_id>", methods=["GET"])
def get_coop(coop_id):
    try:
        # Fetch the co-op details from the database
        query = "SELECT * FROM Coops WHERE CoOpID = %s"
        conn = mysql.connector.connect(user="root", password="password", database="startupconnect")
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (coop_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": f"No co-op found with ID {coop_id}"}), 404

        return jsonify(result), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# GET: Retrieve all co-ops
@coop_bp.route("/api/coop_updates", methods=["GET"])
def get_all_coops():
    try:
        # Fetch all co-ops from the database
        query = "SELECT * FROM Coops"
        conn = mysql.connector.connect(user="root", password="password", database="startupconnect")
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        return jsonify(results), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

        # Check if the record was updated
        if cursor.rowcount == 0:
            return jsonify({"error": f"No Co-op found with ID {coop_id}"}), 404

        conn.commit()
        return jsonify({"message": f"Co-op {coop_id} updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
