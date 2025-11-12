#Port that the http server will run on
PORT=8888

#Runs main.py and opens http server on port
python3 src/main.py --verbose
cd docs && python3 -m http.server $PORT