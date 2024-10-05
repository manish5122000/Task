from django.urls import path
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version='v1',
        description="Task management API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

# API's url
    path('tasks/', CreateTaskView.as_view(), name='create_task'),
    
    # Change method here for PUT and DELETE
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('all/tasks/', TaskListView.as_view(), name='task_list'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

# Frontend url
    path('', home , name="home"),
    path('tasks/create/', create_task, name='task_create'),   
    path('tasks/list/', all_task_list, name='task_list_page'),
    path('task/<int:task_id>/', task_by_id, name='task'), 
    path('tasks/update/<int:task_id>/', update_task, name='update_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),  

  

]
