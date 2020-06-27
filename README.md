# Spanish Flu research framework
Using ML techniques to overlay Spanish Flu data on COVID-19. You can find all datasets published in [CoronaWhy Data Lake](http://datasets.coronawhy.org/dataverse/pandemics).
# Video with meetings
We're sharing all meetings on YouTube, please feel free to join us if you would like to contribute.
- [Kick-off #team-social-analysis] (https://www.youtube.com/watch?v=z2RLU9J0Fv0)
- [Discussion about datasets and goals] (https://www.youtube.com/watch?v=8Z7Gm954aVQ&feature=youtu.be)
# Data
Download the latest version of the [KB Spanish flu dataset] (http://datasets.coronawhy.org/dataset.xhtml?persistentId=doi:10.5072/FK2/WPIDZZ)
```
wget http://datasets.coronawhy.org/api/access/datafile/480752 -O data.tar.gz
gzip -cd data.tar.gz|tar xf -
```
# Installation
Download Language Identification Model:
```
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```
Install fasttext module 
```
pip install fasttext
``` 
# Usage
Run Language Detection process
```
python3 ./main.py
```
# CoronaWhy infrastructure
You can also do full-text search in the whole collection by querying Elasticsearch index spanishflu
```
curl "http://search.coronawhy.org/spanishflu/_search?pretty=true&q=*"
```
