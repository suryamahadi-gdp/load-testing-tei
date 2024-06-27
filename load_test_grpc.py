"""
Loadtesting for gRPC server
"""
import grpc
import concurrent.futures
import time
import threading
from argparse import ArgumentParser
import json

from tei_pb2_grpc import RerankStub
from tei_pb2 import RerankRequest, RerankResponse


def dispatch_request(stub: RerankStub, request: RerankRequest) -> RerankResponse:
    try:
        return stub.Rerank(request)
    except grpc.RpcError as e:
        print(e)
        return None




if __name__ == '__main__':
    parser = ArgumentParser(description="Load testing for gRPC server")
    parser.add_argument("--host", default="localhost", help="Host of the server")
    parser.add_argument("--port", default=50051, help="Port of the server")
    parser.add_argument("--num_requests", default=100, help="Number of requests to send")
    parser.add_argument("--concurrency", default=10, help="Number of concurrent requests to send")
    args = parser.parse_args()

    with open("rerank_param.json", "r") as f:
        rerank_param = json.load(f)
    
    num_of_success = 0
    num_of_failed = 0
    response_times = []
    lock = threading.Lock()

    channel = grpc.insecure_channel(f"{args.host}:{args.port}")
    stub = RerankStub(channel)
    request = RerankRequest(query=rerank_param["query"], texts=rerank_param["texts"])

    def make_request():
        global num_of_success, num_of_failed
        start = time.time()
        response = dispatch_request(stub, request)
        end = time.time()

        with lock:
            response_times.append(end - start)
            if response is not None:
                num_of_success += 1
            else:
                num_of_failed += 1

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = []
        for i in range(args.num_requests):
            futures.append(executor.submit(make_request))

        concurrent.futures.wait(futures)

    end_time = time.time()

    print(f"Number of success: {num_of_success}")
    print(f"Number of failed: {num_of_failed}")
    print(f"Average response time: {sum(response_times) / len(response_times)}")
    print(f"Total time: {end_time - start_time}")
    print(f"QPS: {args.num_requests / (end_time - start_time)}")
    print(f"Throughput: {num_of_success / (end_time - start_time)}")
    print(f"Percentile 95: {sorted(response_times)[int(len(response_times) * 0.95)]}")
    print(f"Percentile 99: {sorted(response_times)[int(len(response_times) * 0.99)]}")
    print(f"Mimimum response time: {min(response_times)}")
    print(f"Maximum response time: {max(response_times)}")

    
            





   