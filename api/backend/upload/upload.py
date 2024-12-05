from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "./uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/api/upload_resume", methods=["POST"])
def upload_resume():
    try:
        # Retrieve file and form data
        file = request.files.get("file")
        user_id = request.form.get("user_id")
        notes = request.form.get("notes", "")

        # Validate inputs
        if not file or not user_id:
            return jsonify({"error": "Missing required fields: file or user_id"}), 400

        # Ensure the file has an allowed extension
        if not file.filename.endswith((".pdf", ".docx")):
            return jsonify({"error": "Invalid file type. Only PDF and DOCX are allowed."}), 400

        # Save the file
        save_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_{file.filename}")
        file.save(save_path)

        # Log additional notes (if any)
        if notes:
            notes_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_notes.txt")
            with open(notes_path, "w") as f:
                f.write(notes)

        return jsonify({"message": "Resume uploaded successfully", "path": save_path}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500