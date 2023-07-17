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


class RequestModel(models.Model):
    STATE_NEW = 0
    STATE_MANUALLY_FILTERED = 1
    STATE_AUTO_FILTERED = 2
    STATE_IN_PROGRESS = 3
    STATE_NOT_PARTICIPATING_OBJECTIVELY = 4
    STATE_NOT_PARTICIPATING_SUBJECTIVELY = 5
    STATE_BID_SUBMISSION = 6
    STATE_BID_SUBMITTED = 7
    STATE_AUCTION = 8
    STATE_AUCTION_COMPLETED_RETURN_SECURITY = 9
    STATE_AUCTION_COMPLETED = 10
    STATE_CONTRACT_SIGNING = 11
    STATE_CONTRACT_SIGNED = 12
    STATE_CONTRACT_EXECUTED = 13


    states = {
        STATE_NEW: _('New'),
        STATE_MANUALLY_FILTERED: _('Manually Filtered'),
        STATE_AUTO_FILTERED: _('Automatically Filtered'),
        STATE_IN_PROGRESS: _('In Progress'),
        STATE_NOT_PARTICIPATING_OBJECTIVELY: _('Not Participating (Objective)'),
        STATE_NOT_PARTICIPATING_SUBJECTIVELY: _('Not Participating (Subjective)'),
        STATE_BID_SUBMISSION: _('Bid Submission'),
        STATE_BID_SUBMITTED: _('Bid Submitted'),
        STATE_AUCTION: _('Auction'),
        STATE_AUCTION_COMPLETED_RETURN_SECURITY: _('Auction Completed (Return Security)'),
        STATE_AUCTION_COMPLETED: _('Auction Completed'),
        STATE_CONTRACT_SIGNING: _('Contract Signing'),
        STATE_CONTRACT_SIGNED: _('Contract Signed'),
        STATE_CONTRACT_EXECUTED: _('Contract Executed'),
    }

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
    state = FSMIntegerField(default=STATE_NEW, choices=states.items())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_name

    def state_name(self):
        return self.states[self.state]
