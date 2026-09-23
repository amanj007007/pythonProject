from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("api/tasks/", views.task_list_api, name="task-list"),
    path("tasks/<int:task_id>/", views.task_detail, name="task-detail"),
]