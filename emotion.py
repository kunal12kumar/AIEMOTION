import spacy  #this is to do tokonization of the text and indentifying the grammer in this 
import torch

import pyttsx3 # this is to convert text into speech. by this we can only control speed, volume and voice(man ,women) of the speech.

from transformers import pipeline  #here it is used for ner(named entity recognition)

from flask import Flask, request, jsonify  #this is to import data from javascript file

from flask_cors import CORS    #this is when browser does not allow to export data for security purpose then we use to export data easily to other file.


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/data": {"origins": "http://localhost:8000"}})

#here we are importing data from javascript file
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json  #here we are converting stringfy data into object.
    
    print(f"Received data: {data}")  # printing the data which is in dictionary form
    
    value=data.get('key')   # here extracting the from the dictionary sentence  which we input 
    
    print(f"Value of 'key': {value}") #printing the sentence
    # Process the data as needed
    

    
    # Load SpaCy model
    nlp = spacy.load("en_core_web_sm")  #this is to load english language

    # Load pre-trained emotion detection model
    emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

    def get_emotions(text):
        # Process the text with SpaCy
        doc = nlp(text)
        
        # Get emotion scores
        emotions = emotion_pipeline(text)   #this give the dictonary of emotion and its score after the tokenization of the sentence
        
        return emotions

    # Example usage
    text = value  #here we are intializing the input to text to use by the getemoti
    emotions = get_emotions(text) #calling the function to do work on given argument (sentence)
    print(emotions) #printing the array containing the  dictionary(emotion and their score)
    for emotion in emotions[0]:
        print(f"{emotion['label']}: {emotion['score']:.4f}")  #printing it as dictionary by extracting it form array
        
    # Initialize the TTS engine
    engine = pyttsx3.init()  #here we are starting the pyttsx3. to convert our text to speech

    
        # Determine the dominant emotion
    emotion=emotions[0]  #here we are destructuring the array to get the value(emotion and its score ) from it .
    dominant_emotion = max(emotion, key=lambda x: x["score"]) #here we are filtering the emotion which has maximum score.

    # Your sentenced
    sentence = value   #passing the value to pyttsx3 to convert it into the speech
    

    # Set properties based on the dominant emotion
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}")

# Set a specific voice (example using the first available voice)
    engine.setProperty('voice', voices[1].id)
    if dominant_emotion['label'] == 'joy':
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1.0)  # Volume of speech
    elif dominant_emotion['label'] == 'sadness':
        engine.setProperty('rate', 100)
        engine.setProperty('volume', 0.5)
    elif dominant_emotion['label'] == 'anger':
        engine.setProperty('rate', 165)
        engine.setProperty('volume', 0.85)
    elif dominant_emotion['label'] == 'fear':
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.6)
    elif dominant_emotion['label'] == 'surprise':
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 0.9)
    else:  # Neutral or any other emotion
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 0.9)

    # Convert the sentence to speech
    engine.say(sentence)
    engine.runAndWait()

        
    return jsonify({"status": "success", "data": data})


# Sample emotions and their respective probabilities


if __name__ == '__main__':
    app.run(debug=True)


