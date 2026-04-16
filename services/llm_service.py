import google.generativeai as genai
from config.settings import Settings

# Configure Gemini
genai.configure(api_key=Settings.GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel(Settings.MODEL_NAME)


def get_ai_response(messages: list) -> str:
    """
    Converts chat-style messages into a single prompt for Gemini
    and returns the generated response.
    """

    try:
        prompt_text = ""

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt_text += f"[SYSTEM]\n{content}\n\n"
            elif role == "user":
                prompt_text += f"[USER]\n{content}\n\n"
            elif role == "assistant":
                prompt_text += f"[ASSISTANT]\n{content}\n\n"

        response = model.generate_content(prompt_text)

        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"