from django.db import models
from django.contrib.auth.models import User
import json


class Drc_error(models.Model):
    error_names = models.TextField(default = "[]")

    def get_error_names(self):
        return json.loads(self.error_names)

    def set_error_names(self, error_names):
        self.error_names = json.dumps(error_names)

    errors_names = property(get_error_names, set_error_names)


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.TextField(max_length=100, default='')

class ProductionStep(models.TextChoices):
    OPTION_1 = 'notYet', 'Yet to be started'
    OPTION_2 = 'started', 'Just started'
    OPTION_3 = 'metalisation', 'Metalisation'
    OPTION_4 = 'almost', 'Almost finishied'
    OPTION_5 = 'finished', 'Finished'


class ResultFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, default=None)
    zippedGerbers = models.FileField(upload_to='uploads/')
    zippedDrills = models.FileField(upload_to='uploads/')
    DRCresult = models.FileField(upload_to='uploads/')
    ERCresult = models.FileField(upload_to='uploads/')
    pdf_file = models.FileField(upload_to='uploads/', default='uploads/test.pdf')
    description = models.TextField(max_length=100, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.TextField(max_length=100, default='')
    valid = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    locked = models.BooleanField(default=False)
    Errors = models.OneToOneField(Drc_error, on_delete=models.CASCADE)
    isToProduce = models.BooleanField(default=False)
    isInProduction = models.BooleanField(default=False)
    isProduced = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    productionStep = models.CharField(
        max_length=12,
        choices=ProductionStep.choices,
        default=ProductionStep.OPTION_1
    )

    def __str__(self):
        return self.filename

    def next_step(self):
        j = 0
        for i in range(len(ProductionStep.choices)):
            if ProductionStep.choices[i] == self.productionStep:
                j = i
                break
        self.productionStep = ProductionStep.choices[j] if j < len(ProductionStep.choices) else len(ProductionStep.choices) - 1


class AuthorizedError(models.Model):
    error_names = models.TextField(unique=True)

    def get_error_names(self):
        return json.loads(self.error_names)

    def set_error_names(self, error_names):
        self.error_names = json.dumps(error_names)

    authorized_error_names = property(get_error_names, set_error_names)


class ModelList(models.Model):
    error_names = models.TextField()

    def get_values(self):
        return json.loads(self.error_names)

    def set_values(self, error_names):
        self.error_names = json.dumps(error_names)

    values = property(get_values, set_values)

class PanelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.TextField(max_length=100, default='') 
    description = models.TextField(default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result_files = models.ManyToManyField(ResultFile)
    amounts = models.OneToOneField(ModelList, on_delete=models.CASCADE, default=0)
    panel_file = models.FileField(upload_to='Panels/')
    zippedGerbers = models.FileField(upload_to='uploads/', default='zzccmxtp.zip')
    zippedDrills = models.FileField(upload_to='uploads/', default='zzccmxtp.zip')    
    kicad_pcb = models.FileField(upload_to='uploads/', default='zzccmxtp.zip')   
    Errors = models.OneToOneField(Drc_error, on_delete=models.CASCADE)
    
     
    isToProduce = models.BooleanField(default=False)
    isInProduction = models.BooleanField(default=False)
    isProduced = models.BooleanField(default=False)
    productionStep = models.CharField(
        max_length=12,
        choices=ProductionStep.choices,
        default=ProductionStep.OPTION_1
    )

    def next_step(self):
        j = 0
        for i in range(len(ProductionStep.choices)):
            if ProductionStep.choices[i] == self.productionStep:
                j = i
                break
        self.productionStep = ProductionStep.choices[j] if j < len(ProductionStep.choices) else len(ProductionStep.choices) - 1
        return j < len(ProductionStep.choices)


    def __str__(self):
        return self.filename
    
    def update_status(self):
        for result_file in self.result_files.all():
            result_file.isInProduction = self.isToProduce
            result_file.isProduced = self.isProduced
            result_file.productionStep = self.productionStep
    
class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    staff_response = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    co_users = models.ManyToManyField(User, related_name='co_tickets', blank=True)
    reopened = models.BooleanField(default=False)
    reopen_requested = models.BooleanField(default=False)
    result_file = models.OneToOneField(ResultFile, on_delete=models.CASCADE, blank=True, null=True, default=None)
    panel_file = models.OneToOneField(PanelFile, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return self.title
    
class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answeredByStaff = models.BooleanField(default=False)

    def __str__(self):
        return self.content