
import json
import re
from pathlib import Path


# Load the FAQ dataset
def load_faq():
    file_path = Path(__file__).parent / "sample_faq.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: sample_faq.json was not found.")
        return {"greetings": ["hello", "hi"], "faqs": []}
    except json.JSONDecodeError:
        print("Error: The FAQ JSON file has invalid formatting.")
        return {"greetings": ["hello", "hi"], "faqs": []}


data = load_faq()


# Normalize user input
def normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())


# Identify all matching intents
def identify_intents(message):
    patterns = {
        "greeting": r"\b(hello|hi|hey|good morning|good afternoon)\b",
        "hours": r"\b(hours|opening time|closing time|open|close|working hours)\b",
        "project": r"\b(project|submit|submission|github|repository)\b",
        "certificate": r"\b(certificate|certification|completion|when.*certificate)\b",
        "thanks": r"\b(thanks|thank you|thx)\b",
        "help": r"\b(help|support|assist)\b"
    }

    return [
        intent
        for intent, pattern in patterns.items()
        if re.search(pattern, message)
    ]


# Find an FAQ answer using keyword matching
def find_faq(message):
    words = set(re.findall(r"\b[a-z0-9]+\b", message))
    best_answer = None
    best_score = 0

    for faq in data.get("faqs", []):
        question_words = set(
            re.findall(r"\b[a-z0-9]+\b", faq["question"].lower())
        )

        # Ignore common words
        common_words = {
            "what", "are", "your", "the", "how", "do",
            "i", "when", "will", "my", "is", "a", "to"
        }

        useful_words = question_words - common_words
        score = len(words & useful_words)

        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    if best_score >= 1:
        return best_answer

    return None


# Generate a response
def get_response(user_input):
    message = normalize(user_input)

    if not message:
        return "Please type a question."

    # Exit commands
    if re.fullmatch(r"(bye|exit|quit)", message):
        return "Goodbye! Thank you for chatting with us."

    intents = identify_intents(message)
    responses = []

    if "greeting" in intents:
        responses.append("Hello! Welcome to our support assistant.")

    if "thanks" in intents:
        responses.append("You're welcome! Happy to help.")

    if "help" in intents:
        responses.append(
            "I can answer questions about business hours, "
            "internship project submission, and certificates."
        )

    # Search FAQs for relevant answers
    faq_answer = find_faq(message)

    if faq_answer:
        responses.append(faq_answer)

    if responses:
        return "\n".join(responses)

    return (
        "Sorry, I didn't understand your question. "
        "Please ask about business hours, project submission, "
        "or certificates."
    )


# Main chatbot conversation
def main():
    print("=" * 45)
    print("       RULE-BASED CHATBOT ASSISTANT")
    print("=" * 45)
    print("Type 'bye', 'exit', or 'quit' to end the chat.")
    print("You can ask about hours, projects, or certificates.")

    while True:
        try:
            user_input = input("\nYou: ")
            response = get_response(user_input)

            print("Bot:", response)

            if re.fullmatch(
                r"(bye|exit|quit)", normalize(user_input)
            ):
                break

        except (EOFError, KeyboardInterrupt):
            print("\nBot: Chat ended. Goodbye!")
            break


if __name__ == "__main__":
    main()
