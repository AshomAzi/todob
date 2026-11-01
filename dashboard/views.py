from django.shortcuts import render, redirect
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