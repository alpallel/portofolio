from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Project
from main.forms import ProjectForm


def show_main(request):
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
        "experience_list": Experience.objects.all()
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Alfarrel Ersya Balawa",
        "short_name": "Alfarrel",
        "projects_list": Project.objects.all(),
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
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
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")