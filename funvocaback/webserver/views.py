from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Word
from .serializers import CustomerSerializer, WordSerializer
import socket
import threading

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/word-list/',
        'Detail View' : '/word-detail/<str:pk>',
        'Create' : '/word-create/',
        'Update' : '/word-update/<str:pk>',
        'Delete' : '/word-delete/<str:pk>',
        }
    return Response(api_urls)

@api_view(['GET'])
def wordList(request):
    words = Word.objects.all()
    serializer = WordSerializer(words, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def wordDetail(request, pk):
    words = Word.objects.get(id=pk)
    serializer = WordSerializer(words, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def wordCreate(request):
    serializer = WordSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)

@api_view(['POST'])
def wordUpdate(request, pk):
    word = Word.objects.get(id=pk)
    serializer = WordSerializer(instance = word, data = request.data)

    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)

@api_view(['DELETE'])
def wordDelete(request, pk):
    word = Word.objects.get(id=pk)
    word.delete()
        
    return Response('Item has succsesfully deleted!')






@api_view(['GET'])
def helloAPI(request):
    return Response("hello world")


@api_view(['GET'])
def RandomCustomer(request):
    return Response("hello world")


def chatServer(request):
    # Connection Data
    #host = '15.165.171.194'
    port = 7777

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen()

    # Lists For Clients and Their Nicknames
    clients = []
    nicknames = []

    # Sending Messages To All Connected Clients
    def broadcast(message):
        for client in clients:
            client.send(message)

    # Handling Messages From Clients
    def handle(client):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                broadcast(message)
            except:
                # Removing And Closing Clients
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break

    # Receiving / Listening Function
    def receive():
        while True:
            # Accept Connection
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            print("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    receive()
    message = "수 하나를 입력해주세요."
    return HttpResponse(message)

