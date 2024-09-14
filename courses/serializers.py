from rest_framework import serializers

from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'number', 'type', 'name',  'start_date', 'end_date', 'location', 'year', 'federation')
