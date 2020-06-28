import fasttext
import json 
import os
import re
from codecs import encode
from tqdm import tqdm
from ast import literal_eval
from config import citationfile, years, DEBUG, keywords, DATA_PATH, PRETRAINED_MODEL_PATH, languages
import chardet
from language_extracter import language_extractions

model = fasttext.load_model(PRETRAINED_MODEL_PATH)

overall_stats = dict()
sentdict = {}

if not DEBUG:
    citations = open(citationfile, "w+")

for root,dirs,files in os.walk(DATA_PATH, topdown=True):
    for name in tqdm(files):
        with open(os.path.join(DATA_PATH,name),mode="r+") as f:
            try:
                data = json.load(f)
            except:
                print("File %s has errors" % os.path.join(DATA_PATH,name))
                continue

            # Default is to process all years, use filter on yeas in config.py otherwise
            if re.match(years, data['date']):
                if DEBUG:
                    print("Publication date: %s" % data['date'])
                x = literal_eval(data['text'])
                temp = x.decode('utf-8').split('\r\n')
                all_sentences = []
                for i in temp:
                    all_sentences.extend(i.split('\n'))
                sentences = []
                for item in (all_sentences):
                    for keyword in keywords:
                        if re.search(keyword, item, re.IGNORECASE):
                            if not item in sentdict:
                                sentences.append(item)
                                sentdict[item] = name
                                if DEBUG:
                                    print("[%s] %s" % (data['date'], item))
                                else:
                                    try:
                                        citation = "\"%s\"\n\tSource: %s, %s, %s" % (item, data['alternative'], data['date'], data['url'])
                                    except KeyError:
                                        print ("File name: {} has insufficient attributes, adding just source urn".format(os.path.join(DATA_PATH,name)))
                                        citation = "\"%s\"\n\tSource: %s" % (item, data['url'])

                                    citations.write("%s\n\n" % citation)
            
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
                    #print (name)
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
            

if not DEBUG:
    citations.close()
print (overall_stats)

#Running separate language extraction to check english sentences
language_extractions(languages,model,keywords)



