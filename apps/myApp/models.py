from django.db import models
from django.db.models.deletion import SET_NULL
from ..loginApp.models import User

class JobManager(models.Manager):

    def job_validator(self,post_data):
        errors = {}

        field_name = "title"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Title is required!"
        elif len(field_value)<=3 or len(field_value)>100:
            errors[field_name] = "Title must be between 4 and 100 characters."

        field_name = "description"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Description is required!"
        elif len(field_value)<=10 or len(field_value)>200:
            errors[field_name] = "Description must be between 10 and 200 characters."

        field_name = "location"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Location is required!"

        return errors

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    location = models.CharField(max_length=100)
    job_posted_by = models.ForeignKey(User,related_name='posted_jobs',on_delete=models.CASCADE)
    job_taken_by = models.ForeignKey(User,related_name='taken_jobs',on_delete=SET_NULL,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobManager()
