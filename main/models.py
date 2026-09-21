import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    started_at_string = models.CharField(max_length=20, blank=True, null=True)
    ended_at_string = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        if self.ended_at is not None:
            return False
        if not self.ended_at_string or not self.ended_at_string.strip():
            return True
        return self.ended_at_string.strip().lower() in ["present", "sekarang", "saat ini"]

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    thumbnail = models.URLField(blank=True, null=True)
    link = models.URLField()