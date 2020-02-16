import spacy
import en_core_web_lg
import pandas as pd
import numpy as np
import re
import json
import flask
from flask import Flask, request, jsonify, make_response, abort

nlp = en_core_web_lg.load()

app = flask.Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def process_text(text):
    text = text.encode('ascii', errors='ignore').decode()
    text = text.lower()
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'#+', ' ', text )
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
    text = re.sub(r"([A-Za-z]+)'s", r"\1 is", text)
    text = re.sub(r"won't", "will not ", text)
    text = re.sub(r"isn't", "is not ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    return text

def find_semantic_similarity(sent):
    sent = list(map(process_text, sent))
    docs = [nlp(s) for s in sent]
    outer_idx = list(range(len(docs)));
    inner_idx = list(range(len(docs)));
    groups = [];
    match_idx = [];

    for idx in outer_idx:
        if idx not in match_idx:
            temp_group = [sent[idx]]
        else:
            temp_group = []

        for i in inner_idx:
            sim = docs[idx].similarity(docs[i])
            #         print(sent[idx], sent[i], sim)
            if sim > 0.75 and idx != i and idx not in match_idx and i not in match_idx:
                temp_group.append(sent[i])
                match_idx.append(idx)
                match_idx.append(i)
        if len(temp_group) > 0:
            groups.append(temp_group)

    return groups

@app.route('/group_similar_text', methods=['POST'])
def group_similar_text():
    content = request.data
    sent = json.loads(content).get('sentences')
    output = find_semantic_similarity(sent)
    return jsonify(output)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8005, debug=True)