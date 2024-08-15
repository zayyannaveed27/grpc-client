from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc

class GreeterService(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"SayHello Request Made: {request}")
        hello_reply = greet_pb2.HelloReply()
        hello_reply.message = f"{request.greeting} {request.name}"
        return hello_reply
    
    def ParrotSaysHello(self, request, context):
        print(f"ParrotSaysHello Request Made: {request}")
        for i in range(3):
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name} {i+1}"
            yield hello_reply
            time.sleep(3)
    
    def ChattyClientSaysHello(self, request_iterator, context):
        
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("ChattyClientSaysHello Request Made:" + str(request))
            delayed_reply.request.append(request)

        delayed_reply.message = f"Hello you have sent {len(delayed_reply.request)} messages. Please expect a delayed reply."
        return delayed_reply
    
    def InteractingHello(self, request_iterator, context):
        for request in request_iterator:
            print(f"InteractingHello Request Made: {request}")
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name}"
            yield hello_reply
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()