import pandas as pd
from rank_bm25 import BM25Okapi
import numpy as np

df=pd.read_csv("Friends dialogues.csv")
corpus=df['Dialogue'].tolist()
tokenized_corpus = [doc.split(" ") for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

def search(query):
    query=query.lower()
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    index=np.argsort(-doc_scores)[:5][0]
    return df.iloc[index][0],df.iloc[np.argsort(-doc_scores)[:5][2]][0]

q=input("Enter the dialogue to search episode : ")
episode,e=search(str(q))
print(episode,e)