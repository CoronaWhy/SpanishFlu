import fasttext
import json 
import os
import re
from codecs import encode
from tqdm import tqdm
from ast import literal_eval
from config import citationfile, DEBUG, keywords, DATA_PATH, PRETRAINED_MODEL_PATH
import chardet

'''
Extract all sentences of specified language with optional filters for deeper analysis
'''

def language_extractions(languages, model, filters=[]):
    for lang in languages:
        language_sentences = open('{}_detected_sentences.txt'.format(lang),"w+")
        for root,dirs,files in os.walk(DATA_PATH, topdown=True):
            for name in tqdm(files):
                with open(os.path.join(DATA_PATH,name),mode="r") as f:
                    try:
                        data = json.load(f)
                    except:
                        print("File %s has errors" % os.path.join(DATA_PATH,name))
                        continue
                    x = literal_eval(data['text'])
                    temp = x.decode('utf-8').split('\r\n')
                    all_sentences = []
                    for i in temp:
                        all_sentences.extend(i.split('\n'))
                    sentences = []
                    for item in all_sentences:
                        prediction = model.predict(item)
                        lang_detected = prediction[0][0].replace('__label__','')
                        if lang_detected == lang:
                            if len(filters)>0:
                                if any(keyword in item.lower() for keyword in filters):
                                    sentences.append(item)
                                    to_write = "\"%s\"\n\tSource: %s" % (item, data['url'])
                                    language_sentences.write("%s\n\n" % to_write)
                            else:   
                                sentences.append(item)
                                to_write = "\"%s\"\n\tSource: %s" % (item, data['url'])
                                language_sentences.write("%s\n\n" % to_write)
