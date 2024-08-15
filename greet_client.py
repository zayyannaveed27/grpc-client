import greet_pb2
import greet_pb2_grpc
import time
import grpc

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
            print("Not implemented")
        elif choice == "3":
            print("Not implemented")
        elif choice == "4":
            print("Not implemented")
        else:
            print("Invalid choice")


if __name__ == '__main__':
    run()

