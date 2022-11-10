import random

from flask import Flask
from flask import request
from flask import Response
import numpy as np
from pymode import text_check
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import requests
from keras.models import load_model

TOKEN = "5776507197:AAGL6GEfEMahMnTdmIouGOl_HDEcH7GsM5w"
app = Flask(__name__)
model = load_model(r"C:\Users\rocki\Desktop\CL_FINAL_PROJECT\model00000250.h5")
data = open('master_new.txt', 'r', encoding='utf8').read()
corpus = data.lower().split("\n")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus)
noise = 1


def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


def generate_poetry(seed_text):
    global noise
    next_words = 50
    output_text = ""
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences(
            [token_list], maxlen=274 - 1,
            padding='pre')
        predicted = np.argmax(model.predict(token_list,
                                            verbose=1), axis=-1)
        output_word = ""

        for word, ind in tokenizer.word_index.items():
            if ind == predicted:
                output_word = word
                break

        seed_text += " " + output_word
        out_text = " "
    print(noise)
    if noise == 2:
        noise = 1
        out_text
        return out_text
    noise += 1
    out_text = text_check(seed_text)
    return out_text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)
        if txt == "/start" or txt == "/restart":
            tel_send_message(chat_id,
                             "👋 Welcome!!!\nI am  Alpha-00x1.\nI was developed by:\nVidit, Jitendra, Shivani and Aditya to generate poems based on given seed text.\n\n"
                             + "I was developed using Machine Learning technologies like LSTM,RNN and NLP and I am currently in alpha version.\n")
            tel_send_message(chat_id,
                             "Help me with first few words 🗨️ and I will send you a poem 📝.\n\n\n")
            tel_send_message(chat_id,
                             "Disclaimer:Current accuracy I achieved is 76.66%. Due to the unavailability of powerful GPUs 🔥 and the fact that I am just a machine learning model 🤖, I may not provide you with poems, as wonderful as written by"
                             + " Robert Frost or Emily Dickinson.\nRest I assure I will provide you with phrase regardless of what you send as a seed text😇.\n\n\nEnter your text:")
        elif txt == '/retry':
            tel_send_message(chat_id, 'Enter your text.')
        else:
            msg = generate_poetry(txt)
            tel_send_message(chat_id, msg)
            tel_send_message(chat_id, 'type /retry to try again.')

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
