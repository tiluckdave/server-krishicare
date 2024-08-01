from flask_restful import Resource
from flask import request, jsonify
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyCedk7pWXZNeLgM0X9K5XzqOiiFOZcnm5E")

# Initialize conversation history
messages = []

# Create a model instance
geminiModel = genai.GenerativeModel('gemini-1.0-pro-latest')

class ChatBot(Resource):
    def post(self):
        try:
            input_text = request.json.get("input")
            messages.append({"role": "user", "content": input_text})
            print(messages)

            # Generate response using Google Generative AI
            prompt = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in messages])
            response = geminiModel.generate_content(prompt)
            response_text = response.text

            # Add the model's response to the conversation history
            messages.append({"role": "assistant", "content": response_text})

            return jsonify({"success": True, "message": response_text})
        except Exception as error:
            print("Error processing request:", error)
            return jsonify({"success": False, "message": "Internal Server Error"}), 500
