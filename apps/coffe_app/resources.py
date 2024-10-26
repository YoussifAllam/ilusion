# myapp/resources.py

from import_export import resources
from .models import User_model

class MyModelResource(resources.ModelResource):
    class Meta:
        model = User_model
        # You can specify fields, exclude fields, import_id_fields, etc.
