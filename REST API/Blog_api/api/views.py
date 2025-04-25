from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import *
from api.serializer import *
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class UserAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            if request.user.is_superuser:
                users = User.objects.all()
                s_users = UserSerializer(users, many=True)
                return Response({"message":"Data fetched Successfully", "Users":s_users.data}, status=status.HTTP_200_OK)
            else:
                s_user = UserSerializer(request.user)
                return Response({"message":"Data fetched Successfully", "User":s_user.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            s_user = UserSerializer(data=request.data)
            if not s_user.is_valid():
                return Response({"message":"Verification failed, check input!", "errors":s_user.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_user.save()
            return Response({"message":"User created succesfully!", "data":s_user.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

    def patch(self, request):
        try:
            user_id = request.data.get('id')

            if request.user.is_superuser and user_id:
                user = get_object_or_404(User, pk=user_id) 
            else:
                user = request.user

            s_user = UserSerializer(user, data=request.data, partial=True)
            if not s_user.is_valid():
                return Response({"message":"Verification failed, check input!", "errors":s_user.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_user.save()
            return Response({"message":"User updated succesfully!", "data":s_user.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        try:
            if not request.user.is_superuser:
                return Response({"message": "You don't have permission to perform this task!"}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = request.data.get('id')
            if not user_id:
                return Response({"message": "User ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, pk=user_id)
            s_user = UserSerializer(user) 
            user.delete()

            return Response({"message": "User deleted successfully!", "data": s_user.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.all()
            s_blogs = BlogSerializer(blogs, many=True)
            return Response({"message":"Data fetched Successfully", "Blogs":s_blogs.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            s_blog = BlogSerializer(data=request.data, context={'request': request})
            if not s_blog.is_valid():
                return Response({"message":"Verification failed, check input!", "errors":s_blog.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_blog.save()
            return Response({"message":"Blog added succesfully!", "data":s_blog.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ModifyBlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:
            blog = get_object_or_404(Blog, pk=id)
            s_blog = BlogSerializer(blog)
            return Response({"message": "Blog fetched successfully!", "data": s_blog.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, id):
        try:
            blog = get_object_or_404(Blog, pk=id)
            if request.user == blog.author:
                s_blog = BlogSerializer(blog, data=request.data, partial=True)
                if not s_blog.is_valid():
                    return Response({"message":"data verification failed, check input!", "errors":s_blog.errors}, status=status.HTTP_400_BAD_REQUEST)
                s_blog.save()
                return Response({"message":"Blog Updated succesfully!", "data":s_blog.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"You dont have permission to edit this blog"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id):
        try:
            blog = get_object_or_404(Blog, pk=id)

            if request.user.is_superuser or request.user == blog.author:
                s_blog = BlogSerializer(blog)
                blog.delete()
                return Response({"message": "Blog deleted successfully", "data": s_blog.data}, status=status.HTTP_200_OK)
            
            return Response({"message": "You don't have permission to delete this blog"}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserBlogsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(author=request.user)
            s_blogs = BlogSerializer(blogs, many=True)
            return Response({"message": f"Blogs by {request.user.username}", "Blogs": s_blogs.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, b_id):
        try:
            flag = request.query_params.get('flag')
            if flag == "all":
                if not request.user.is_superuser:
                    return Response({"message": "You are not authorized to view all comments."}, status=status.HTTP_403_FORBIDDEN)
                comments = Comment.objects.all()
                message = "All Comments"
            else:
                blog = get_object_or_404(Blog, pk=b_id)
                comments = Comment.objects.filter(blog=blog)
                message = f"Comments on Blog: {blog.id} - {blog.title}"
            
            s_comments = CommentSerializer(comments, many=True)
            return Response({"message": message, "Comments": s_comments.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, b_id):
        try:
            blog = get_object_or_404(Blog, pk=b_id)
            s_comment = CommentSerializer(data=request.data)
            if not s_comment.is_valid():
                return Response({"message":"Verification failed, check input!", "errors":s_comment.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_comment.save(author=request.user, blog=blog)
            return Response({"message":f"Comment added succesfully on blog: {blog.id} - {blog.title}", "data":s_comment.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ModifyCommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, c_id):
        try:
            comment = get_object_or_404(Comment, pk=c_id)
            if request.user == comment.author:
                s_comment = CommentSerializer(comment, data=request.data, partial=True)
                if not s_comment.is_valid():
                    return Response({"message":"data verification failed", "errors":s_comment.errors}, status=status.HTTP_400_BAD_REQUEST)
                s_comment.save()
                return Response({"message":'Comment updated succesfully', "data":s_comment.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"You dont have permission to edit this comment"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, c_id):
        try:
            comment = get_object_or_404(Comment, pk=c_id)
            
            if request.user.is_superuser or request.user==comment.author:
                s_comment = CommentSerializer(comment)
                comment.delete()
                return Response({"message":"comment deleted succesfully", "data":s_comment.data}, status=status.HTTP_204_NO_CONTENT)
            
            return Response({"message":"You dont have permission to delete this blog"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserCommentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            comments = Comment.objects.filter(author=request.user)
            s_comments = CommentSerializer(comments, many=True)
            return Response({"message": f"Comments by {request.user.username}", "Comments": s_comments.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    




class LikeAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, b_id):
        try:
            blog = get_object_or_404(Blog, pk=b_id)
            likes = Like.objects.filter(blog=blog)
            s_likes = LikeSerializer(likes, many=True)
            return Response({"message":f"Likes on blog: {blog.id} - {blog.title}", "Likes":s_likes.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, b_id):
        try:
            blog = get_object_or_404(Blog, pk=b_id)
            s_like = LikeSerializer(data=request.data)
            if not s_like.is_valid():
                    return Response({"message":"data verification failed", "errors":s_like.errors}, status=status.HTTP_400_BAD_REQUEST)
            s_like.save(blog=blog, user=request.user)
            return Response({"message":f'liked blog: {blog.id} - {blog.title}', "data":s_like.data}, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({"message": "You have already liked this blog."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, b_id):
        try:
            blog = get_object_or_404(Blog, pk=b_id)
            like = Like.objects.get(blog=blog, user=request.user)
            
            if request.user == like.user:
                s_like = LikeSerializer(like)
                like.delete()
                return Response({"message": "Like removed successfully", "data": s_like.data}, status=status.HTTP_204_NO_CONTENT)

            return Response({"message": "You don't have permission to perform this task"}, status=status.HTTP_403_FORBIDDEN)
        
        except Like.DoesNotExist:
                return Response({"message": "You haven't liked this blog yet."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLikesAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            likes = Like.objects.filter(user=request.user)
            s_likes = LikeSerializer(likes, many=True)
            return Response({"message":f"Data fetched successfully", "Likes":s_likes.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           