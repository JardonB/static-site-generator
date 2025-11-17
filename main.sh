#Port that the http server will run on
PORT=8888
BASEPATH="/"

#Runs main.py and opens http server on $PORT
python3 src/main.py $BASEPATH --verbose
cd docs && python3 -m http.server $PORT