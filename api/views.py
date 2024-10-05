from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from django.contrib import messages  

from rest_framework.response import Response
from rest_framework import status
from .models import *
from drf_yasg.utils import swagger_auto_schema
from .serializers import TaskSerializer

# Create Task API
class CreateTaskView(APIView):
    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":201,"message": "Task Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Task API's
class TaskDetailView(APIView):
    def get_object(self, task_id):
        try:
            return TaskModel.objects.get(id=task_id)
        except TaskModel.DoesNotExist:
            return None

# Get Task API by Id
    def get(self, request, task_id):
        task = self.get_object(task_id)
        if task is None:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response({"status":200, "message": "Successfully","data":serializer.data})

# Update Task API
    @swagger_auto_schema(request_body=TaskSerializer)
    def put(self, request, task_id):
        task = self.get_object(task_id)
        if task is None:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "message": "Task Updated Successfully","data":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Delete Task API
    def delete(self, request, task_id):
        task = self.get_object(task_id)
        if task is None:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({"status":200, "message": "Task Deleted Successfully"})


# Get All Task API
class TaskListView(APIView):
    def get(self, request):
        tasks = TaskModel.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"status":200, "message": "Successfully","data":serializer.data})


# Home Page
def home(request):
    return render(request,"index.html")

# Create Task via Frontend
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        task = TaskModel(title=title, description=description)
        task.save()
        messages.success(request, "Task created successfully!")
        return redirect('task_create')  

    return render(request, "create_task.html")

# All task list via frontend
def all_task_list(request):
    tasks = TaskModel.objects.all()  
    return render(request, "task_list.html", {'tasks': tasks}) 

# Get task by Id via Frontend
def task_by_id(request, task_id):
    task = get_object_or_404(TaskModel, id=task_id)  
    return render(request, "task.html", {'task': task})

# Update task via frontend
def update_task(request, task_id):
    task = get_object_or_404(TaskModel, id=task_id) 

    if request.method == 'POST':
        task.title = request.POST.get('title') 
        task.description = request.POST.get('description')  
        task.save()  
        messages.success(request, "Task updated successfully!")  
        return redirect('task_list_page')  

    return render(request, "update_task.html", {'task': task})  

# Delete Task via frontend
def delete_task(request, task_id):
    task = get_object_or_404(TaskModel, id=task_id)  
    task.delete() 
    messages.success(request, 'Task deleted successfully!') 
    return redirect('task_list_page')

