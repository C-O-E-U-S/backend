# from urllib import request
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)
load_dotenv()
# Set up the OpenAI API key
openai.api_key = "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"
# openai.api_key = "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"
model_engine = "text-davinci-002"

# Endpoint for processing user queries
@app.route("/query", methods=["POST"])
def query_bot():
    # Get the user query from the request body
    user_query = request.json["query"]
    
    # Call OpenAI's GPT-3 API to generate a response
    response = openai.Completion.create(
        engine=model_engine,
        prompt=user_query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    )
    
    # Extract the response text from the API response
    bot_response = response.choices[0].text.strip()
    
    # Return the bot response to the client
    return jsonify({"response": "Give detailed answer of the following question : " + bot_response})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
