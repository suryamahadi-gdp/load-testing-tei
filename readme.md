# Installation
```bash
pip install -r requirements.txt
```

# Run Load Testing
```bash
 python load_test_grpc.py --host localhost --port 8081 --concurrency 10 --num_requests 100
```

This will run 100 requests with 10 concurrent requests to the server running on localhost:8081

# Example output
```
Number of success: 100
Number of failed: 0
Average response time: 0.46377755641937257
Total time: 4.812337160110474
QPS: 20.77992390660017
Throughput: 20.77992390660017
Percentile 95: 0.6736483573913574
Percentile 99: 0.7618603706359863
Mimimum response time: 0.3430795669555664
Maximum response time: 0.7618603706359863
```