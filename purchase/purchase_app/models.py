from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMIntegerField


class PurchaseFilesModel(models.Model):
    filename = models.TextField(blank=True, null=True)
    file_date = models.TextField(blank=True, null=True)
    import_date = models.TextField(blank=True, null=True)
    record_count = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)


class PurchasePlanModel(models.Model):
    externalId = models.TextField(unique=True)
    planNumber = models.TextField(blank=True, null=True)
    versionNumber = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    archive_name = models.TextField(blank=True, null=True)


class PurchaseModel(models.Model):
    externalId = models.TextField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    purchase_object_info = models.TextField(blank=True, null=True)
    publish_year = models.IntegerField(blank=True, null=True)
    purchase_files = models.IntegerField(blank=True, null=True)
    purchase_files_obj = models.ForeignKey(PurchaseFilesModel, on_delete=models.CASCADE, blank=True, null=True)
    externalId_obj = models.ForeignKey(PurchasePlanModel, to_field='externalId', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['externalId'], name='unique_externalId'),
        ]


class StateRequestModel(models.Model):

    STATE_CHOICES = [
        ('New', 'New'),
        ('Manually Filtered', 'Manually Filtered'),
        ('Automatically Filtered', 'Automatically Filtered'),
        ('In Progress', 'In Progress'),
        ('Not Participating (Objective)', 'Not Participating (Objective)'),
        ('Not Participating (Subjective)', 'Not Participating (Subjective)'),
        ('Bid Submission', 'Bid Submission'),
        ('Bid Submitted', 'Bid Submitted'),
        ('Auction', 'Auction'),
        ('Auction Completed (Return Security)', 'Auction Completed (Return Security)'),
        ('Auction Completed', 'Auction Completed'),
        ('Contract Signing', 'Contract Signing'),
        ('Contract Signed', 'Contract Signed'),
        ('Contract Executed', 'Contract Executed'),
    ]
    
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        state_mappings = {
            'New': (0, 'Статус при обработке новой заявки'),
            'Manually Filtered': (1, 'Заявка не подходит (отсеивается вручную)'),
            'Automatically Filtered': (2, 'Заявка не подходит (отсеивается алгоритмом)'),
            'In Progress': (3, 'Заявки интересна, идет изучение документации'),
            'Not Participating (Objective)': (4, 'В заявке есть критические моменты, которые не позволяют взять в работу'),
            'Not Participating (Subjective)': (5, 'Не берем в работу по субъективным причинам, например: не успеем сделать, не хватает компетенций, не достаточная стоимость контракта, нет средств на обеспечение и т.д.'),
            'Bid Submission': (6, 'Идет процесс подачи заявки на ЭТП'),
            'Bid Submitted': (7, 'Заявка подана на ЭТП, ожидание даты начала торгов'),
            'Auction': (8, 'Идут торги. Устанавливается автоматически за час до начала торгов и висит до момента внесения информации о итогах'),
            'Auction Completed (Return Security)': (9, 'Торги завершены, ожидание возврата обеспечения'),
            'Auction Completed': (10, 'Торги завершены, обеспечение возвращено'),
            'Contract Signing': (11, 'Идет процесс подписания контракта'),
            'Contract Signed': (12, 'Контракт подписан, идет процесс выполнения'),
            'Contract Executed': (13, 'Контракт завершен'),
        }

        self.order, self.description = state_mappings.get(self.name, (0, ''))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class RequestModel(models.Model):
    registry_number = models.CharField(
        verbose_name='Реестровый номер извещения', max_length=75
    )
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
    contract_completion_date = models.DateTimeField(verbose_name='Дата выполнения контракта', blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    state = models.ForeignKey(StateRequestModel, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_name

    def state_name(self):
        return self.states[self.state]
