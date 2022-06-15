curl http://127.0.0.1:5000/jinja
sleep 1
curl http://127.0.0.1:5000/tempylate
sleep 1
ab -c 10 -n 1000 http://127.0.0.1:5000/jinja
sleep 1
ab -c 10 -n 1000 http://127.0.0.1:5000/tempylate