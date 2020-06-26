import fasttext
import json 
import os
from codecs import encode
from tqdm import tqdm
from ast import literal_eval
import chardet

DATA_PATH = 'data'

PRETRAINED_MODEL_PATH = 'lid.176.bin'
model = fasttext.load_model(PRETRAINED_MODEL_PATH)

overall_stats = dict()

for root,dirs,files in os.walk(DATA_PATH, topdown=True):
    for name in tqdm(files):
        with open(os.path.join(DATA_PATH,name),mode="r+") as f:
            data = json.load(f)
            x = literal_eval(data['text'])
            temp = x.decode('utf-8').split('\r\n')
            all_sentences = []
            for i in temp:
                all_sentences.extend(i.split('\n'))
            sentences = []
            for item in (all_sentences):
                if len(item)>20:
                    sentences.append(item)
            
            predictions = model.predict(sentences)
            doc_lang = dict()

            for i in range(len(sentences)):
                if predictions[1][i][0]>0.7:
                    key = predictions[0][i][0].replace('__label__','')
                    if key in doc_lang:
                        doc_lang[key] += 1
                    else:
                        doc_lang[key] = 1

            doc_lang = {k: v for k, v in sorted(doc_lang.items(), key=lambda item: item[1], reverse=True)}
            if len(doc_lang)==0:
                print (name)
                identified_lang = 'failed_to_identify'
            else:
                identified_lang = list(doc_lang)[0]
            data['lang_iso'] = identified_lang
            if identified_lang in overall_stats:
                overall_stats[identified_lang] += 1
            else:
                overall_stats[identified_lang] = 1

            f.seek(0)
            f.truncate()
            json.dump(data,f)
            

print (overall_stats)



