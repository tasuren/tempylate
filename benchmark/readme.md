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
| Time per request | 0.458ms   | 0.534ms |

### Detail
I was pasted the results from the terminal here.
#### tempylate
```terminal
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
Document Length:        2445 bytes

Concurrency Level:      10
Time taken for tests:   0.534 seconds
Complete requests:      1000
Failed requests:        824
   (Connect: 0, Receive: 0, Length: 824, Exceptions: 0)
Total transferred:      2620001 bytes
HTML transferred:       2445001 bytes
Requests per second:    1872.11 [#/sec] (mean)
Time per request:       5.342 [ms] (mean)
Time per request:       0.534 [ms] (mean, across all concurrent requests)
Transfer rate:          4789.98 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       6
Processing:     1    5   2.1      5      21
Waiting:        1    5   2.0      4      16
Total:          1    5   2.1      5      21

Percentage of the requests served within a certain time (ms)
  50%      5
  66%      5
  75%      6
  80%      6
  90%      7
  95%     10
  98%     13
  99%     14
 100%     21 (longest request)

# tempylate
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
Document Length:        1449 bytes

Concurrency Level:      10
Time taken for tests:   0.458 seconds
Complete requests:      1000
Failed requests:        823
   (Connect: 0, Receive: 0, Length: 823, Exceptions: 0)
Total transferred:      1624005 bytes
HTML transferred:       1449005 bytes
Requests per second:    2183.05 [#/sec] (mean)
Time per request:       4.581 [ms] (mean)
Time per request:       0.458 [ms] (mean, across all concurrent requests)
Transfer rate:          3462.19 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       1
Processing:     1    4   1.6      4      14
Waiting:        1    4   1.5      4      13
Total:          1    5   1.6      4      14

Percentage of the requests served within a certain time (ms)
  50%      4
  66%      4
  75%      5
  80%      5
  90%      6
  95%      8
  98%     11
  99%     12
 100%     14 (longest request)
 ```