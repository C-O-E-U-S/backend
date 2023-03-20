# from urllib import request
from flask import Flask, jsonify, request
import os
from Image_process import lavis
import openai

app = Flask(__name__)
load_dotenv()
# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "text-davinci-003"

@app.route("/api/image-process", methods=["POST"])
def image_process():
    from werkzeug.utils import secure_filename
    # from werkzeug.datastructures import  FileStorage
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save("upload_temp_" + filename)
    user_query_img = lavis.classify("upload_temp_" + filename)
    # return user_query_img
    # return (lavis.do_shit("hello beech"))
    response = openai.Completion.create(
        engine=model_engine,
        prompt="I will give you a statement. If it is a question give a detailed answer with all possible outcomes else if it a statement, give a detailed exaggerated version of it. QUERY: " + user_query_img[0],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    )
    
    # # Extract the response text from the API response
    bot_response_img = response.choices[0].text.strip()
    # if os.path.exists("demofile.txt"):
    os.remove("upload_temp_" + filename)
    # # Return the bot response to the client
    return jsonify({"response": bot_response_img})
    
    

# Endpoint for processing user queries
@app.route("/api/generate-answer", methods=["POST"])
def query_bot():
    
    # Get the user query from the request body
    user_query = request.json["query"]
    
    # Call OpenAI's GPT-3 API to generate a response
    response = openai.Completion.create(
        engine=model_engine,
        prompt="I will give you a statement. If it is a question give a detailed answer with all possible outcomes else if it a statement, give a detailed exaggerated version of it. QUERY: " + user_query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    )
    
    # Extract the response text from the API response
    bot_response = response.choices[0].text.strip()
    
    # Return the bot response to the client
    return jsonify({"response": bot_response})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
