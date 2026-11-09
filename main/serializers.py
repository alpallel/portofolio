from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project


class ExperienceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    liked_by_names = serializers.SerializerMethodField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "organization",
            "started_at_string",
            "ended_at_string",
            "is_ongoing",
            "likes_count",
            "is_liked",
            "liked_by_names",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "category_display", "is_ongoing"]
        extra_kwargs = {
            "thumbnail": {"required": False, "allow_blank": True, "allow_null": True},
            "organization": {"required": False, "allow_blank": True, "allow_null": True},
            "started_at_string": {"required": False, "allow_blank": True, "allow_null": True},
            "ended_at_string": {"required": False, "allow_blank": True, "allow_null": True},
        }

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_organization(self, value):
        return strip_tags(value).strip() if value else value

    def validate_started_at_string(self, value):
        return strip_tags(value).strip() if value else value

    def validate_ended_at_string(self, value):
        return strip_tags(value).strip() if value else value

    def get_likes_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.liked_by.all()

    def get_liked_by_names(self, obj):
        return ", ".join(user.username for user in obj.liked_by.all())

    def get_star_count(self, obj):
        return self.get_likes_count(obj)

    def get_is_starred(self, obj):
        return self.get_is_liked(obj)

    def get_starred_by_names(self, obj):
        return self.get_liked_by_names(obj)


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "link", "thumbnail",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
