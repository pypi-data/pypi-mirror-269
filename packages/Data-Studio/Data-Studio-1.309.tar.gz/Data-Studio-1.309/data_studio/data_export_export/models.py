from django.db import models
from django.contrib.auth.models import User

class DataExport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_exports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    file_path = models.FileField(upload_to='exports/', blank=True, null=True)
    project_id = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'data_export_export'
