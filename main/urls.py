from django.urls import path

from main.views import (
    show_main, 
    show_experience, 
    create_experience,
    get_experiences_json,
    delete_experience,
    show_projects, 
    create_project, 
    get_projects_json, 
    delete_project,
    )

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    path("experience/", show_experience, name="show_experience"),
    path("experience/add", create_experience, name="create_experience"),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/",delete_experience,name="delete_experience"),

    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project")
]