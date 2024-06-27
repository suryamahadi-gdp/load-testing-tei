# Installation
```bash
pip install -r requirements.txt
```

# Run Load Testing
```bash
 python load_test_grpc.py --host localhost --port 8081 --concurrency 10 --num_requests 100
```

This will run 100 requests with 10 concurrent requests to the server running on localhost:8081