
import google.generativeai as genai
import re 


genai.configure(api_key="AIzaSyAfZpA0FGlcl2HoMU1wlfsTk8GyIIyFRnI")

def setup_model():
    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

def remove_formatting(text):
    # Remove markdown and HTML tags
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[*_`~]', '', text)   # Remove markdown formatting symbols
    return text

def chat():
    model = setup_model()
    convo = model.start_chat(history=[])
    user_input = input("You: ")
    while user_input.lower() != "exit":
        convo.send_message(user_input)
        response = convo.last.text
        response_plain_text = remove_formatting(response)
        print("AI:", response_plain_text)
        user_input = input("You: ")

if __name__ == "__main__":
    chat()
