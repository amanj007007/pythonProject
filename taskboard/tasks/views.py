from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Task


def home(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "tasks/home.html", {"tasks": tasks})


def task_list_api(request):
    data = [
        {
            "id": t.id,
            "title": t.title,
            "done": t.done,
            "due_date": t.due_date,
        }
        for t in Task.objects.all()
    ]

    return JsonResponse({"tasks": data})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    return render(
        request,
        "tasks/detail.html",
        {"task": task},
    )