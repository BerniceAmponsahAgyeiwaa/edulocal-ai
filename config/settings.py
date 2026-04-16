import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """
    Central configuration for the EduLocal AI system.
    """

    # 🔑 Gemini API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    # 🤖 Model Configuration
    MODEL_NAME = "models/gemini-2.5-flash"

    # 🎛️ Inference Controls
    TEMPERATURE = 0.3
    TOP_P = 0.9
    MAX_TOKENS = 500

    # 🌍 Supported Languages
    SUPPORTED_LANGUAGES = ["English", "Twi", "Ewe"]

    # 📚 Defaults
    DEFAULT_LANGUAGE = "English"
    DEFAULT_DIFFICULTY = "simple"

    # 📝 Logging
    LOG_FILE_PATH = "data/logs.json"