import greet_pb2
import greet_pb2_grpc
import time
import grpc

def get_client_stream_requests():
    while True:
        name = input("Enter a name (or nothing to stop chatting): ")
        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("--------------")
        print("1. SayHello - Unary")
        print("2. ParrotSaysHello - Server Streaming")
        print("3. ChattyClientSaysHello - Client Streaming")
        print("4. InteractingHello - Bidirectional Streaming")
        print("--------------")
        choice = input("Which rpc would you like to call: ")

        if choice == "1":
            hello_request = greet_pb2.HelloRequest(greeting="Hello", name="World")
            hello_reply = stub.SayHello(hello_request)
            print("Say Hello Response Received: " + hello_reply.message)
        elif choice == "2":
            hello_request = greet_pb2.HelloRequest(greeting="Hello", name="World")
            hello_replies = stub.ParrotSaysHello(hello_request)
            for reply in hello_replies:
                print("ParrotSaysHello Response Received: " + reply.message)
        elif choice == "3":
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())
            print("ChattyClientSaysHello Response Received: ")
            print(delayed_reply)

        elif choice == "4":
            responses = stub.InteractingHello(get_client_stream_requests())
            for response in responses:
                print("InteractingHello Response Received: " + response.message)
        else:
            print("Invalid choice")


if __name__ == '__main__':
    run()

