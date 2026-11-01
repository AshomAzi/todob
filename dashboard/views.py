from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def dashboard(request):

    if request.method == "POST":
        Task.objects.create(
        user=request.user,
        title = request.POST.get("title"),
        description = request.POST.get("description"),
        due_date = request.POST.get("due_date"),
        priority = request.POST.get("priority"),
        )
        return redirect("dashboard")


    my_task=Task.objects.filter(user=request.user)

    return render(request, "dashboard.html", {"tasks":my_task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method=="POST":
        task.delete()
    return redirect("dashboard")