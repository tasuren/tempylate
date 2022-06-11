curl http://127.0.0.1:5000/jinja
curl http://127.0.0.1:5000/tempylate
ab -c 10 -n 1000 http://127.0.0.1:5000/jinja
ab -c 10 -n 1000 http://127.0.0.1:5000/tempylate