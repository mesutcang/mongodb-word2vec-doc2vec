# Installing dependencies
sudo easy_install pip
pip install -r requirements.txt

## Used libraries

used 
pymongo
gensim


# Running mongodbw
docker pull mongo
docker run -it -p 27017:27017 mongo

# Running application
python main.py