from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from api.models import *
from api.serializer import *

# ✅ User Registration
@api_view(['POST'])
def registerUser(request):
    try:
        s_user = UserSerializer(data=request.data)
        if not s_user.is_valid():
            return Response({"status": "400", "errors": s_user.errors, "message": "Validation failed. Please check the input."}, status=status.HTTP_400_BAD_REQUEST)
        s_user.save()
        return Response({"message": "User registered successfully. Please log in to get your token.", "data": s_user.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Fetch User(s) (Admin vs. Non-Admin)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    try:
        user_id = request.query_params.get('id')
        user = request.user
        if user.is_superuser:
            users = User.objects.filter(pk=user_id) if user_id else User.objects.all()
        else:
            if user_id:
                if str(user.id) == user_id:
                    users = User.objects.filter(pk=user.id)
                else:
                    return Response({"error": "You don't have permission to access this user."}, status=status.HTTP_403_FORBIDDEN)
            else:
                users = User.objects.filter(pk=user.id)
        return Response({"Users": UserSerializer(users, many=True).data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Todo CRUD Operations
class TodoAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # ✅ Retrieve Todo(s)
    def get(self, request):
        try:
            user = request.user
            task_id = request.query_params.get('id')

            if user.is_superuser:                      # Admin: Can access any task(s)
                tasks = Todo.objects.filter(pk=task_id) if task_id else Todo.objects.all()
            else:
                if task_id:                             # Non-Admin: Can only access their own tasks
                    tasks = [get_object_or_404(Todo, pk=task_id, user=user)]
                else:
                    tasks = Todo.objects.filter(user=user)
            s_tasks = TodoSerializer(tasks, many=True)
                
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Create Todo
    def post(self, request):
        try:
            s_task = TodoSerializer(data=request.data, context={'request': request})
            if not s_task.is_valid():
                return Response({"status": "400", "errors": s_task.errors, "message": "Validation failed. Check input."}, status=status.HTTP_400_BAD_REQUEST)
            s_task.save(user=request.user)
            return Response({"message": "Task added successfully.", "data": s_task.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Update Todo (Partial Update)
    def patch(self, request, task_id):
        try:
            task = get_object_or_404(Todo, pk=task_id, user=request.user)
            s_task = TodoSerializer(task, data=request.data, partial=True)
            if not s_task.is_valid():
                return Response({"status": "400", "errors": s_task.errors, "message": "Validation failed. Check input."}, status=status.HTTP_400_BAD_REQUEST)
            s_task.save()
            return Response({"message": "Task updated successfully.", "data": s_task.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Delete Todo
    def delete(self, request, task_id):
        try:
            task = get_object_or_404(Todo, pk=task_id, user=request.user)
            task.delete()
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



            