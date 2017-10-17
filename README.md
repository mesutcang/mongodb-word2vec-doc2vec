# Installing dependencies
sudo easy_install pip

pip install -r requirements.txt

## Used libraries

pymongo
gensim


# Running mongodb
docker pull mongo

docker run -it -p 27017:27017 mongo

# Running application
python main.py