from rest_framework import serializers
from courses.models import Subject, Course
from django.db.models import Count

class SubjectSerializer(serializers.ModelSerializer):
    total_courses = serializers.IntegerField()
    popular_courses =serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        courses = obj.courses.annotate(
            total_students=Count('students')
            ).order_by('total_students')[:3]
        return [
            f'{c.title} ({c.total_students})' for c in courses
            ]
    
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']

        class CourseSerializer(serializers.ModelSerializer):
            class Meta:
                fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']