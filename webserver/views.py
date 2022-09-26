from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Word
from .serializers import CustomerSerializer, WordSerializer

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


