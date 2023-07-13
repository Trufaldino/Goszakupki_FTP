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
        ('new', 'Новая'),
        ('manually_filtered', 'Отфильтрована (вручную)'),
        ('auto_filtered', 'Отфильтрована (автоматически)'),
        ('in_progress', 'В работе'),
        ('not_participating_objectively', 'Не участвуем (объективно)'),
        ('not_participating_subjectively', 'Не участвуем (субъективно)'),
        ('bid_submission', 'Подача заявки'),
        ('bid_submitted', 'Заявка подана'),
        ('auction', 'Торги'),
        ('auction_completed_return_security', 'Торги завершены (возврат обеспечения)'),
        ('auction_completed', 'Торги завершены'),
        ('contract_signing', 'Подписание контракта'),
        ('contract_signed', 'Контракт подписан'),
        ('contract_executed', 'Контракт исполнен'),
    )

    registry_number = models.PositiveBigIntegerField(verbose_name='Реестровый номер извещения')
    purchase_name = models.TextField(verbose_name='Наименование закупки')
    initial_price = models.PositiveBigIntegerField(verbose_name='Начальная цена')
    bid_security_amount = models.PositiveIntegerField(
        verbose_name='Размер обеспечения заявки', blank=True, null=True
    )
    work_security_amount = models.PositiveIntegerField(
        verbose_name='Размер обеспечения работ', blank=True, null=True
    )
    warranty_security_amount = models.PositiveIntegerField(
        verbose_name='Размер обеспечения гарантии', blank=True, null=True
    )
    warranty_period = models.PositiveSmallIntegerField(verbose_name='Срок гарантии', blank=True, null=True)
    bid_submission_deadline = models.DateTimeField(
        verbose_name='Дата и время окончания срока подачи заявок (dd.mm.YYYY mm:hh) timedate (UTC)'
    )
    contract_completion_date = models.DateField(verbose_name='Дата выполнения контракта', blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    status = models.CharField(verbose_name='Статус', max_length=150, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_name
