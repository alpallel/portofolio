from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 
import datetime

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm


def show_main(request):
    last_login = request.COOKIES.get('last_login', '-')
    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "npm": "2506656406",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer di Universitas Indonesia. "
            "Saya selalu terbuka untuk mengeksplorasi bidang baru dan menemukan "
            "bagaimana teknologi dapat memecahkan masalah nyata tanpa harus mengetahui "
            "segalanya sekaligus."
        ),
        "experience_list": Experience.objects.all(),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def is_editor(user):
    return user.is_authenticated and (
        user.groups.filter(name="Editor").exists()      # AI digunakan untuk mencari solusi Django group filtering
        or user.has_perm("main.change_experience")      # AI menyarankan untuk menambah line ini
    )


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "experience_list": experiences,
        "title_query": title_query,
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):

    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "form": form,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def edit_experience(request, experience_id):

    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_experience(request, experience_id):

    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/")
def create_project(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):

    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_like(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.liked_by.all():
            experience.liked_by.remove(request.user)
        else:
            experience.liked_by.add(request.user)

    return redirect("main:show_experience")