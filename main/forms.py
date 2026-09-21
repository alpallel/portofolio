from django.forms import ModelForm, TextInput, Textarea, URLInput, Select

from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "thumbnail",
            "link",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "thumbnail": "URL Gambar Proyek",
            "link": "URL Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "https://github.com/alpallel/projectorsomething",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "organization",
            "started_at_string",
            "ended_at_string",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "thumbnail": "URL Gambar Pengalaman",
            "organization": "Organisasi Pengalaman",
            "started_at_string": "Tanggal Mulai",
            "ended_at_string": "Tanggal Berakhir (kosongkan jika masih berlanjut)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff of ...",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "COMPFEST",
                    "maxlength": 255,
                }
            ),
            "started_at_string": TextInput(
                attrs={
                    "placeholder": "Apr 2026",
                    "maxlength": 20,
                }
            ),
            "ended_at_string": TextInput(
                attrs={
                    "placeholder": "Sep 2026",
                    "maxlength": 20,
                }
            ),
        }