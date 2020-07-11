from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS,cross_origin
import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi

app = Flask(__name__,static_url_path='/static')
@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        query=request.form['q']
        query=str(query).lower()
        df = pd.read_csv("Friends dialogues.csv")
        corpus = df['Dialogue'].tolist()
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = query.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        index = np.argsort(-doc_scores)[:5][0]
        more_episodes= df.iloc[np.argsort(-doc_scores)[:5][2]][0]
        #return df.iloc[index][0]
        return render_template('results.html', episode=df.iloc[index][0], dialogue=query)


if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5000))
    app.debug=True
    app.run()