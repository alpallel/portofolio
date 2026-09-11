from main.models import Experience

Experience.objects.create(
    title="Staff of Software Engineering Academy",
    description="Membantu persiapan teknis dan seleksi peserta acara Software Engineering Academy COMPFEST18",
    category="volunteer",
    organization="COMPFEST", 
)

Experience.objects.create(
    title="Mentor",
    description="Membantu mahasiswa baru memahami dasar-dasar pemrograman python sebagai persiapan untuk mata ku4liah DDP1",
    category="volunteer",
    organization="Dasar-Dasar Pemrograman 0",
)

Experience.objects.create(
    title="Intern Staff at Departement of Information Technology",
    description="Mempelajari backend framework Django di kegiatan Sekolah BEM Fasilkom",
    category="internship",
    organization="BEM Fasilkom UI",
)

from main.models import Projects

Projects.objects.create(
    title="Web Judol Attack Checker",
    description="Sitemap scanner that detects online gambling keyword injections across website URLs. Generates detailed JSON reports for security audits.",
    link="https://github.com/alpallel/Web-Judol-Attack-Checker",
)

Projects.objects.create(
    title="Pathsim for Linux",
    description="PathSim installation for Linux Operating System.",
    link="https://github.com/alpallel/PathSim-for-linux",
)

from django.contrib.auth.models import User

# Delete a specific superuser by username
User.objects.get(username="your_username", is_superuser=True).delete()
