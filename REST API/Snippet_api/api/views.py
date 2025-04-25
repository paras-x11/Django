from django.shortcuts import render, get_object_or_404
from api.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from api.serializer import *
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
@api_view(['POST'])
def registerUser(request):
    try:
        s_user = UserSerializer(data=request.data)
        if not s_user.is_valid():
            return Response({"status":"400", "errors":s_user.errors, "message":"Validation failed!, check input!"}, status=status.HTTP_400_BAD_REQUEST)
        s_user.save()
        return Response({"message":"User Added Successfully", "data":s_user.data}, status=status.HTTP_201_CREATED)
   
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def getUsers(request):
    try:
        user = request.user
        if user.is_superuser:
            users = User.objects.all()
            s_users = UserSerializer(users, many=True)
        else:
            s_users = UserSerializer(user)
        return Response({"Users": s_users.data}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUser(request, id):
    try:
        user = get_object_or_404(User, pk=id)
        s_user = UserSerializer(user)
        return Response({"Users": s_user.data}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSnippet(request, id):
    try:
        snippet = get_object_or_404(Snippet, pk=id)
        s_snippet = SnippetSerializer(snippet)
        return Response({"Snippet": s_snippet.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSnippets(request):
    try:
        snippets = Snippet.objects.all()
        s_snippets = SnippetSerializer(snippets, many=True)
        return Response({"Snippets": s_snippets.data}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addSnippet(request):
    try:
        s_snippet = SnippetSerializer(data=request.data, context={'request': request})
        if not s_snippet.is_valid():
            return Response({"status":"400", "errors":s_snippet.errors, "message":"Validation failed!, check input!"}, status=status.HTTP_400_BAD_REQUEST)
        s_snippet.save()
        return Response({"message":"Snippet Added Successfully", "data":s_snippet.data}, status=status.HTTP_201_CREATED)
   
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateSnippet(request, id):
    try:
        snippet = get_object_or_404(Snippet, pk=id)

        if request.user != snippet.user and not request.user.is_superuser:
            return Response({"message": "You do not have permission to update this snippet."}, status=status.HTTP_403_FORBIDDEN)
        
        s_snippet = SnippetSerializer(snippet, data=request.data, partial=True, context={'request': request})
        if not s_snippet.is_valid():
            return Response({"errors": s_snippet.errors, "message": "Validation failed! Check input."}, status=status.HTTP_400_BAD_REQUEST)
        s_snippet.save()
        return Response({"message": "Snippet Updated Successfully", "data": s_snippet.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def deleteSnippet(request, id): 
    try:
        snippet = get_object_or_404(Snippet, pk=id)
        if request.user != snippet.user and not request.user.is_superuser:
            return Response({"message": "You do not have permission to delete this snippet."}, status=status.HTTP_403_FORBIDDEN)
        
        s_snippet = SnippetSerializer(snippet)
        snippet.delete()
        return Response({"message":"Snippet Deleted Successfully", "data":s_snippet.data}, status=status.HTTP_200_OK) 
        
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postComment(request, s_id):
    try:
        snippet = get_object_or_404(Snippet, pk=s_id)
        s_comment = CommentSerializer(data=request.data)
        if not s_comment.is_valid():
            return Response({"status":"400", "errors":s_comment.errors, "message":"Validation failed!, check input!"}, status=status.HTTP_400_BAD_REQUEST)
        s_comment.save(user=request.user, snippet=snippet)
        return Response({"message":f"Comment Added Successfully on {snippet.id}: {snippet}", "data":s_comment.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCommentsBySnippet(request, s_id):
    try:
        snippet = get_object_or_404(Snippet, pk=s_id)
        comments = Comment.objects.filter(snippet=snippet)
        s_comments = CommentSerializer(comments, many=True)
        return Response({"message":f"Comments on {snippet.id}: {snippet}", "data":s_comments.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCommentsByUser(request):
    try:
        comments = Comment.objects.filter(user=request.user)
        s_comments = CommentSerializer(comments, many=True)
        return Response({"message":f"Comments of {request.user}", "data":s_comments.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def updateComment(request, c_id):
    try:
        comment = get_object_or_404(Comment, pk=c_id)
        snippet = comment.snippet
        s_comment = CommentSerializer(comment, data=request.data)
        if not s_comment.is_valid():
            return Response({"status":"400", "errors":s_comment.errors, "message":"Validation failed!, check input!"}, status=status.HTTP_400_BAD_REQUEST)
        s_comment.save()
        return Response({"message":f"Comment Updated Successfully on {snippet.id}: {snippet}", "data":s_comment.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def deleteComment(request, c_id): 
    try:
        comment = get_object_or_404(Comment, pk=c_id)
        snippet = comment.snippet
        if request.user != comment.user and not request.user.is_superuser:
            return Response({"message": "You do not have permission to delete this snippet."}, status=status.HTTP_403_FORBIDDEN)
        
        s_comment = CommentSerializer(comment)
        comment.delete()
        return Response({"message":f"Comment Deleted Successfully on {snippet.id}: {snippet}", "data":s_comment.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
