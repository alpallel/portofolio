from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin_user",
            email="admin@example.com",
            password="password123",
        )
        self.regular_user = User.objects.create_user(
            username="regular_user",
            password="password123",
        )
        self.editor_user = User.objects.create_user(
            username="editor_user",
            password="password123",
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor_user.groups.add(self.editor_group)

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.projects = Project.objects.create(
            title="cool project",
            description="very kul",
            link="https://github.com/alpallel/portofolio",
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
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, reverse("main:get_experiences_json"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertEqual(data[0]["fields"]["title"], self.experience.title)
        self.assertEqual(data[0]["fields"]["description"], self.experience.description)
        self.assertEqual(data[0]["fields"]["category_display"], "Part-Time")
        self.assertTrue(data[0]["fields"]["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("main:get_experiences_json")).json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.experience.is_ongoing)
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertFalse(data[0]["fields"]["is_ongoing"])

    def test_create_experience_page_renders_form(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Tambah Pengalaman Baru")
        self.assertContains(response, "Nama Pengalaman")

    def test_create_experience_post_success(self):
        self.client.force_login(self.superuser)
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
        self.assertContains(response, "Pengalaman baru berhasil ditambahkan!")
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertIn(
            "Software Engineering Intern",
            [item["fields"]["title"] for item in data],
        )

    def test_experience_search_filter(self):
        Experience.objects.create(
            title="atmin fesnuk",
            description="6767",
            category="part-time",
        )
        response = self.client.get(reverse("main:get_experiences_json") + "?title=atmin")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["fields"]["title"] for item in response.json()],
            ["atmin fesnuk"],
        )

    def test_experience_page_renders_delete_button(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        placeholder = "00000000-0000-0000-0000-000000000000"
        self.assertContains(response, reverse("main:delete_experience", args=[placeholder]))
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertTrue(data[0]["fields"]["can_delete"])

    def test_delete_experience_post_success(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())
        self.assertContains(response, "Pengalaman berhasil dihapus!")

    def test_experience_page_renders_edit_button(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        placeholder = "00000000-0000-0000-0000-000000000000"
        self.assertContains(response, reverse("main:edit_experience", args=[placeholder]))
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertTrue(data[0]["fields"]["can_edit"])

        self.client.force_login(self.editor_user)
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertTrue(data[0]["fields"]["can_edit"])
        self.assertFalse(data[0]["fields"]["can_delete"])

    def test_edit_experience_page_renders_form_with_instance(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("main:edit_experience", args=[self.experience.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Edit Pengalaman")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)

    def test_edit_experience_post_success(self):
        self.client.force_login(self.superuser)
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
        self.assertContains(response, "Pengalaman berhasil diperbarui!")
        data = self.client.get(reverse("main:get_experiences_json")).json()
        self.assertIn("CEO", [item["fields"]["title"] for item in data])

    def test_experience_authorization_roles(self):
        self.assertEqual(self.client.get(reverse("main:create_experience")).status_code, 302)
        self.assertEqual(
            self.client.get(reverse("main:edit_experience", args=[self.experience.id])).status_code,
            302,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_experience", args=[self.experience.id])).status_code,
            302,
        )

        self.client.force_login(self.regular_user)
        self.assertEqual(self.client.get(reverse("main:create_experience")).status_code, 403)
        self.assertEqual(
            self.client.get(reverse("main:edit_experience", args=[self.experience.id])).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_experience", args=[self.experience.id])).status_code,
            403,
        )

        self.client.force_login(self.editor_user)
        self.assertEqual(self.client.get(reverse("main:create_experience")).status_code, 403)
        self.assertEqual(
            self.client.get(reverse("main:edit_experience", args=[self.experience.id])).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_experience", args=[self.experience.id])).status_code,
            403,
        )

    def test_toggle_experience_like(self):
        like_url = reverse("main:toggle_like", args=[self.experience.id])

        guest_response = self.client.post(like_url)
        self.assertEqual(guest_response.status_code, 302)

        self.client.force_login(self.regular_user)
        self.client.post(like_url)
        self.assertIn(self.regular_user, self.experience.liked_by.all())
        self.assertEqual(self.experience.liked_by.count(), 1)

        self.client.post(like_url)
        self.assertNotIn(self.regular_user, self.experience.liked_by.all())
        self.assertEqual(self.experience.liked_by.count(), 0)

    def test_projects_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, reverse("api:project-list"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        data = self.client.get(reverse("api:project-list")).json()
        self.assertEqual(data[0]["title"], self.projects.title)
        self.assertEqual(data[0]["description"], self.projects.description)
        self.assertEqual(data[0]["link"], self.projects.link)

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("api:project-list")).json(), [])

    def test_create_project_page_renders_form(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Tambah Proyek Baru")
        self.assertContains(response, "Nama Proyek")

    def test_create_project_post_success(self):
        self.client.force_login(self.superuser)
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
        self.assertContains(response, "Proyek baru berhasil ditambahkan!")
        data = self.client.get(reverse("api:project-list")).json()
        self.assertIn("Pixel Adventure", [item["title"] for item in data])

    def test_project_search_filter(self):
        Project.objects.create(
            title="Minecraft Clone",
            description="Voxel based game engine",
            tech_stack="C++, OpenGL",
            link="https://github.com/alpallel/voxel",
        )
        response = self.client.get(reverse("api:project-list") + "?title=Minecraft")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["title"] for item in response.json()],
            ["Minecraft Clone"],
        )
