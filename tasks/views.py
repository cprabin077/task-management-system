from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import TaskForm
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

    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):

    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()

    pending_tasks = tasks.filter(status="pending").count()

    in_progress_tasks = tasks.filter(status="in_progress").count()

    completed_tasks = tasks.filter(status="completed").count()

    recent_tasks = tasks.order_by("-created_at")[:5]

    context = {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "recent_tasks": recent_tasks,
    }

    return render(request, "tasks/dashboard.html", context)


@login_required
def task_create(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()

            messages.success(request, "Task created successfully.")

            return redirect("task_list")

    else:

        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "page_title": "Create Task",
        },
    )


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": tasks,
        }
    )


@login_required
def task_detail(request, pk):

    task = get_object_or_404(Task, pk=pk, user=request.user)

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
        },
    )


@login_required
def task_update(request, pk):

    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():

            form.save()

            messages.success(request, "Task updated successfully.")

            return redirect("task_detail", pk=task.pk)

    else:

        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/task_form.html",
        {
            "form": form,
            "page_title": "Edit Task",
            "task": task,
        },
    )


@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully."
        )

        return redirect("task_list")

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task,
        }
    )