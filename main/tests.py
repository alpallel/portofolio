from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.projects = Project.objects.create(
                    title="cool project",
                    description="very kul",
                    link="https://github.com/alpallel/portofolio"
                )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_create_experience_page_renders_form(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Tambah Pengalaman Baru")
        self.assertContains(response, "Nama Pengalaman")

    def test_create_experience_post_success(self):
        data = {
            "title": "Software Engineering Intern",
            "description": "anjay masuk gugel",
            "category": "internship",
            "organization": "Google",
            "thumbnail": "https://example.com/logo.png",
            "started_at_string": "Apr 2026",
            "ended_at_string": "Sep 2026",
        }
        response = self.client.post(reverse("main:create_experience"), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertTrue(Experience.objects.filter(title="Software Engineering Intern").exists())
        self.assertContains(response, "Software Engineering Intern")
        self.assertContains(response, "Pengalaman baru berhasil ditambahkan!")

    def test_experience_search_filter(self):
        Experience.objects.create(
            title="atmin fesnuk",
            description="6767",
            category="part-time",
        )
        response = self.client.get(reverse("main:show_experience") + "?title=atmin")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "atmin fesnuk")
        self.assertNotContains(response, "bukan atmin fesnuk")

    def test_experience_page_renders_delete_button(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hapus Pengalaman")
        self.assertContains(response, reverse("main:delete_experience", args=[self.experience.id]))

    def test_delete_experience_post_success(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())
        self.assertContains(response, "Pengalaman berhasil dihapus!")

    def test_experience_page_renders_edit_button(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Pengalaman")
        self.assertContains(response, reverse("main:edit_experience", args=[self.experience.id]))

    def test_edit_experience_page_renders_form_with_instance(self):
        response = self.client.get(reverse("main:edit_experience", args=[self.experience.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Edit Pengalaman")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)

    def test_edit_experience_post_success(self):
        data = {
            "title": "CEO",
            "description": "aku si i o",
            "category": "full-time",
            "organization": "SPPG sebelah preksu",
            "thumbnail": "https://example.com/ta.png",
            "started_at_string": "Jan 2026",
            "ended_at_string": "Jun 2026",
        }
        response = self.client.post(
            reverse("main:edit_experience", args=[self.experience.id]),
            data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "CEO")
        self.assertEqual(self.experience.organization, "SPPG sebelah preksu")
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "CEO")
        self.assertContains(response, "Pengalaman berhasil diperbarui!")

    def test_projects_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.projects.title)
        self.assertContains(response, self.projects.description)
        self.assertContains(response, self.projects.link)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_create_project_page_renders_form(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Tambah Proyek Baru")
        self.assertContains(response, "Nama Proyek")

    def test_create_project_post_success(self):
        data = {
            "title": "Pixel Adventure",
            "description": "A 2D retro RPG game made with Python.",
            "tech_stack": "Python, Pygame",
            "thumbnail": "https://example.com/pixel.png",
            "link": "https://github.com/alpallel/pixel-adventure",
        }
        response = self.client.post(reverse("main:create_project"), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertTrue(Project.objects.filter(title="Pixel Adventure").exists())
        self.assertContains(response, "Pixel Adventure")
        self.assertContains(response, "Proyek baru berhasil ditambahkan!")

    def test_project_search_filter(self):
        Project.objects.create(
            title="Minecraft Clone",
            description="Voxel based game engine",
            tech_stack="C++, OpenGL",
            link="https://github.com/alpallel/voxel",
        )
        response = self.client.get(reverse("main:show_projects") + "?title=Minecraft")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Minecraft Clone")
        self.assertNotContains(response, "cool project")