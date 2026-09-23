from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Task


def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


@login_required
def dashboard(request):

    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()

    pending_tasks = tasks.filter(
        status="pending"
    ).count()

    in_progress_tasks = tasks.filter(
        status="in_progress"
    ).count()

    completed_tasks = tasks.filter(
        status="completed"
    ).count()

    recent_tasks = tasks.order_by("-created_at")[:5]

    context = {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "recent_tasks": recent_tasks,
    }

    return render(
        request,
        "tasks/dashboard.html",
        context
    )