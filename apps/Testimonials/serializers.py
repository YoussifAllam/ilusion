from .models import *
from rest_framework import serializers

class RepliesSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Replaises
        fields = '__all__'

class ADDTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = [ 'id', 'user_name', 'content', 'uploaded_at']



class GetTestimonialSerializer(serializers.ModelSerializer):
    Replies = serializers.SerializerMethodField()

    class Meta:
        model = Testimonials
        fields = ['id', 'user_name', 'content', 'uploaded_at', 'Replies']

    def get_Replies(self, obj):
        replies = Replaises.objects.filter(Testimonial=obj)
        return RepliesSerializer(replies, many=True).data

