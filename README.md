# SpanishFlu research framework
Using ML techniques to overlay Spanish Flu on COVID-19. You can find all datasets published in [CoronaWhy Data Lake](http://datasets.coronawhy.org/dataverse/pandemics)
# Data
Download the latest version of the [KB Spanish flu dataset] (http://datasets.coronawhy.org/dataset.xhtml?persistentId=doi:10.5072/FK2/WPIDZZ)
```
wget http://datasets.coronawhy.org/api/access/datafile/410489 -O data.tar.gz
gzip -cd data.tar.gz|tar xf -
```
# Models
Download Language Identification Model:
```
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```
Install fasttext module 
```
pip install fasttext
``` 
