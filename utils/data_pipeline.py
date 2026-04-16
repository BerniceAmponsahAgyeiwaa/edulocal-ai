import json
import os
from datetime import datetime
from config.settings import Settings


def log_interaction(question: str, response: str, language: str, difficulty: str):
    """
    Logs user interaction for monitoring and evaluation.
    """

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "response": response,
        "language": language,
        "difficulty": difficulty
    }

    file_path = Settings.LOG_FILE_PATH

    try:
        # Create file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        # Read existing logs
        with open(file_path, "r") as f:
            data = json.load(f)

        # Append new log
        data.append(log_entry)

        # Write back
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Logging error: {e}")