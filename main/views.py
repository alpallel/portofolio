from django.shortcuts import render

from main.models import Experience


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
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Alfarrel Ersya Balawa",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)