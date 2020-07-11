import os
import re
import pandas as pd

rootdir = os.getcwd()
episode=[]
text=[]
for subdir, dirs, files in os.walk('Subtitles'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".srt") or filepath.endswith(".sub"):
            #print (filepath)
            name=file[9:-6]
            if name not in episode:
                episode.append(name)
                f=open(filepath)
                data=f.read()
                #data=re.sub(r'{[0-9]+}{[0-9+]}','',data)
                #print(data)
                x=re.findall('[aA-zZ0-9!.,-]+',data)
                dialogue=''
                dialogue=" ".join(x)
                text.append(dialogue)

for subdir, dirs, files in os.walk('Subtitles\Friends - season 10.en'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".srt") or filepath.endswith(".sub"):
            #print (filepath)
            name=file[9:-6]
            if name not in episode:
                episode.append(name)
                f=open(filepath)
                data=f.read()
                #data=re.sub(r'{[0-9]+}{[0-9+]}','',data)
                #print(data)
                x=re.findall('[aA-zZ0-9!.,-]+',data)
                dialogue=''
                dialogue=" ".join(x)
                text.append(dialogue)

print(episode[:24])
print(episode[-10:])
print(len(episode))
#print(text[0])
print(len(text))
dict={'episode':episode,'Dialogue':text}
df=pd.DataFrame(dict)
#print(df.head(5))

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
#STOPWORDS = set(stopwords.words('english'))


def clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    ##text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower()  # lowercase text
    #text=text[31:]
    text = REPLACE_BY_SPACE_RE.sub('', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text

    text=re.sub(r'\d{5,}','',text)

    a=re.split(r'\s{2,}', text)
    t=" ".join(a)
    t = BAD_SYMBOLS_RE.sub('', t)  # delete symbols which are in BAD_SYMBOLS_RE from text
    #text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # delete stopwors from text
    t = re.sub(r'[1-9] 00 00  00 00 ', '', t)
    t=re.sub(r'\d{2,} \d{2,}','',t)
    return t.strip()

print("Before cleaning")
df['Dialogue'].apply(lambda x: len(x.split(' '))).sum()
df['Dialogue'] = df['Dialogue'].apply(clean_text)
print("After Cleaning")
df['Dialogue'].apply(lambda x: len(x.split(' '))).sum()

#print(df.head(5))
df.to_csv("Friends dialogues.csv",index=False)
print("Data Created")