from django.urls import path

from main import api_views

app_name = "api"
urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("experiences/", api_views.experience_list, name="experience-list"),
    path("experiences/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/like/", api_views.experience_like, name="experience-like"),
    path("experiences/<uuid:experience_id>/star/", api_views.experience_like, name="experience-star"),
    path("experience/", api_views.experience_list),
    path("experience/<uuid:experience_id>/", api_views.experience_detail),
    path("experience/<uuid:experience_id>/like/", api_views.experience_like),
    path("experience/<uuid:experience_id>/star/", api_views.experience_like),
]
