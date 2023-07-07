from django.db import models
from django.contrib.auth.models import User


class PurchaseFilesModel(models.Model):
    filename = models.TextField()
    file_date = models.TextField()
    import_date = models.TextField()
    record_count = models.IntegerField()
    status = models.TextField()


class PurchasePlanModel(models.Model):
    externalId = models.TextField(unique=True)
    planNumber = models.TextField()
    versionNumber = models.TextField()
    filename = models.TextField()
    archive_name = models.TextField()


class PurchaseModel(models.Model):
    externalId = models.TextField()
    total_price = models.FloatField()
    purchase_object_info = models.TextField()
    publish_year = models.IntegerField()
    purchase_files = models.IntegerField()
    purchase_files_obj = models.ForeignKey(PurchaseFilesModel, on_delete=models.CASCADE)
    externalId_obj = models.ForeignKey(PurchasePlanModel, to_field='externalId', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['externalId'], name='unique_externalId'),
        ]


class RequestModel(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('rejected', 'Rejected'),
        ('awaiting_auction', 'Awaiting Auction'),
        ('auction_won', 'Auction Won'),
        ('auction_lost', 'Auction Lost'),
    )

    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    auction_date = models.DateField()
    price = models.IntegerField()
    completion_date = models.DateField()
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add the user field

    def __str__(self):
        return self.title
