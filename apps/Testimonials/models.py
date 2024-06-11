from django.db import models
from uuid import uuid4
# Create your models here.
class Testimonials(models.Model) : 
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.user_name

class Replaises(models.Model) : 
    Testimonial = models.ForeignKey(Testimonials, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.user_name


