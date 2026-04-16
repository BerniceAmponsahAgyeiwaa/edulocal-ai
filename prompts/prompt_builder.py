from prompts.system_prompt import SYSTEM_PROMPT
from prompts.few_shot_examples import FEW_SHOT_EXAMPLES


def build_prompt(user_question: str, language: str = "English", difficulty: str = "simple", chat_history: list = None) -> list:
    """
    Builds prompt with:
    - system prompt
    - few-shot examples
    - conversation history (IMPORTANT)
    - current question
    """

    messages = []

    # System
    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })

    # Few-shot
    for example in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": example["question"]})
        messages.append({"role": "assistant", "content": example["answer"]})

    # 🔥 ADD CHAT HISTORY (THIS FIXES YOUR ISSUE)
    if chat_history:
        for msg in chat_history[-6:]:  # limit to last few messages
            messages.append(msg)

    # Instruction
    instruction = f"""
Answer in {language}.
Difficulty: {difficulty}.

Follow format:
- Explanation
- Example

Question:
{user_question}
"""

    messages.append({
        "role": "user",
        "content": instruction.strip()
    })

    return messages