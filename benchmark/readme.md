# Benchmark
## How to use
1. Run `python benchmark` on background.
2. Run `./benchmark.sh`.

## Result
I did benchmark on my pc.

**Environment**
PC: Macbook Air
CPU: M1
RAM: 8GB

### Table
|                  | tempylate | Jinja2  |
|------------------|-----------|---------|
| Time per request | 0.473ms   | 0.504ms |

### Detail
I was pasted the results from the terminal here.
#### tempylates
```terminal
# tempylates
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        Werkzeug/2.1.2
Server Hostname:        127.0.0.1
Server Port:            5000

Document Path:          /tempylate
Document Length:        1448 bytes

Concurrency Level:      10
Time taken for tests:   0.493 seconds
Complete requests:      1000
Failed requests:        832
   (Connect: 0, Receive: 0, Length: 832, Exceptions: 0)
Total transferred:      1623888 bytes
HTML transferred:       1448888 bytes
Requests per second:    2028.52 [#/sec] (mean)
Time per request:       4.930 [ms] (mean)
Time per request:       0.493 [ms] (mean, across all concurrent requests)
Transfer rate:          3216.88 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     2    5   2.3      4      21
Waiting:        2    5   2.3      4      21
Total:          2    5   2.3      4      21

Percentage of the requests served within a certain time (ms)
  50%      4
  66%      5
  75%      5
  80%      5
  90%      7
  95%      9
  98%     13
  99%     15
 100%     21 (longest request)

# Jinja2
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        Werkzeug/2.1.2
Server Hostname:        127.0.0.1
Server Port:            5000

Document Path:          /jinja
Document Length:        2446 bytes

Concurrency Level:      10
Time taken for tests:   0.585 seconds
Complete requests:      1000
Failed requests:        840
   (Connect: 0, Receive: 0, Length: 840, Exceptions: 0)
Total transferred:      2619993 bytes
HTML transferred:       2444993 bytes
Requests per second:    1708.60 [#/sec] (mean)
Time per request:       5.853 [ms] (mean)
Time per request:       0.585 [ms] (mean, across all concurrent requests)
Transfer rate:          4371.61 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     1    6   4.0      5      34
Waiting:        1    5   4.0      4      34
Total:          1    6   4.0      5      34

Percentage of the requests served within a certain time (ms)
  50%      5
  66%      5
  75%      6
  80%      6
  90%      9
  95%     12
  98%     20
  99%     31
 100%     34 (longest request)
 ```