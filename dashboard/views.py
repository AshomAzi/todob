from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# Create your views here.


@login_required
def dashboard(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("dashboard")
    else:
        form = TaskForm()

    my_task = Task.objects.filter(user=request.user)

    return render(request, "dashboard.html", {
        "tasks": my_task,
        "task_form": form,
        "modal_open": bool(request.method == "POST" and form.errors),
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect("dashboard")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(instance=task)

    return render(request, "dashboard.html", {
        "tasks": Task.objects.filter(user=request.user),
        "task_form": form,
        "editing_task": task,
        "modal_open": True,
    })