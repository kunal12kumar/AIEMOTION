import spacy  #this is to do tokonization of the text and indentifying the grammer in this 
import torch

from gtts import gTTS
import os
import pygame



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
    
    
        # Determine the dominant emotion
    emotion=emotions[0]  #here we are destructuring the array to get the value(emotion and its score ) from it .
    dominant_emotion = max(emotion, key=lambda x: x["score"]) #here we are filtering the emotion which has maximum score.
    
    pygame.mixer.init()
    
    
    # Function to generate speech and play it
    def generate_speech(text, emotion):
        if emotion == 'happy':
            tts = gTTS(text=text, lang='en', slow=False)
            filename = 'speech.mp3'
            tts.save(filename)  # faster rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
        elif emotion == 'sad':
            tts = gTTS(text=text, lang='en', slow=True)
            filename = 'speech.mp3'
            tts.save(filename)  # slower rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
        elif emotion == 'angry':
            tts = gTTS(text=text, lang='en', slow=False)
            filename = 'speech.mp3'
            tts.save(filename)  # faster rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
        elif emotion == 'fear':
            tts = gTTS(text=text, lang='en', slow=True)
            filename = 'speech.mp3'
            tts.save(filename)  # moderate rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
        elif emotion == 'disgust':
            tts = gTTS(text=text, lang='en', slow=True)
            filename = 'speech.mp3'
            tts.save(filename)  # slower rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
        elif emotion == 'surprise':
            tts = gTTS(text=text, lang='en', slow=False)
            filename = 'speech.mp3'
            tts.save(filename)  # faster rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
        else:  # default emotion (neutral)
            tts = gTTS(text=text, lang='en', slow=False)
            filename = 'speech.mp3'
            tts.save(filename)  # normal rate

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(filename)  # Clean up the file
            
            
            
    # Save the speech to a file
    

    # Play the speech
    

            
            
    generate_speech(text, dominant_emotion)

    


# Sample emotions and their respective probabilities


if __name__ == '__main__':
    app.run(debug=True)


