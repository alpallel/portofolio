from django.forms import ModelForm, TextInput, Textarea, URLInput, Select
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

    def clean_organization(self):
        return strip_tags(self.cleaned_data.get("organization", "")).strip()

    def clean_started_at_string(self):
        return strip_tags(self.cleaned_data.get("started_at_string", "")).strip()

    def clean_ended_at_string(self):
        return strip_tags(self.cleaned_data.get("ended_at_string", "")).strip()