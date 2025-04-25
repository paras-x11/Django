from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializer import *
from api.models import *

# Create your views here.

@api_view(['GET'])
def getBooks(request):
    books= Book.objects.all()
    s_books = BookSerializer(books, many=True)
    return Response(s_books.data)

@api_view(['POST'])
def addBook(request):
    try:
        s_book = BookSerializer(data=request.data)
        if not s_book.is_valid():
            return Response({'status':'202', 'errors':s_book.errors, 'message':"SomethingWent Wrong"})
        s_book.save()
        return Response({'status':'200', 'data':s_book.data, 'message':"Book Added"})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':"Something Went Wrong"})

@api_view(['PATCH'])
def updateBook(request, id):
    try:
        book = Book.objects.get(pk=id)
        s_book = BookSerializer(book, data=request.data, partial=True)
        if not s_book.is_valid():
            return Response({'status':'202', 'errors':s_book.errors, 'message':"Something Went Wrong"})
        s_book.save()
        return Response({'status':'200', 'data':s_book.data, 'message':"Book Updated"})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':"Something Went Wrong"})

@api_view(['DELETE'])
def deleteBook(request, id):
    try:
        book = Book.objects.get(pk=id)
        s_book = BookSerializer(book)
        if not book:
            return Response({'status':'202', 'errors':s_book.errors, 'message':"Something Went Wrong"})
        book.delete()
        return Response({'status':'200', 'data':s_book.data, 'message':"Book Deleted"})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':"Something Went Wrong"})
    
@api_view(['GET'])
def getBook(request, id):
    try:
        book = Book.objects.get(pk=id)
        s_book = BookSerializer(book)
        return Response({'status':'200', 'data':s_book.data, 'message':f"Book Found: {book}"})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':"Something Went Wrong"})

@api_view(['GET'])
def getBookByAuthor(request, a_id):
    try:
        author = Author.objects.get(pk=a_id)
        books = Book.objects.filter(author=author)
        s_books = BookSerializer(books, many=True)
        return Response({'status':'200', 'data':s_books.data, 'message':""})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':"Something Went Wrong"})

@api_view(['GET'])
def getBookByPublication(request, p_id):
    try:
        publication = Publication.objects.get(pk=p_id)
        books = Book.objects.filter(publication=publication)
        s_books = BookSerializer(books, many=True)
        return Response({'status':'200', 'data':s_books.data, 'message':""})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':"Something Went Wrong"})