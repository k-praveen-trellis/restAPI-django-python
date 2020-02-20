from django.db import models

class Datasheet(models.Model):
    description = models.CharField(max_length=50)
    historical_data = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class Profession(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length =50)
    datasheet = models.OneToOneField(Datasheet, on_delete=models.CASCADE)
    profession = models.ManyToManyField(Profession,default='')
    active = models.BooleanField(default=True)
    
    @property
    def status_message(self):
        if self.active:
            return "Customer is Active"
        else:
            return "Customer is not Active"

    def __str__(self):
        return self.name

    def num_professions(self):
        return self.profession.all().count()
    
class Documents(models.Model):
    DOC_TYPES = [('PP','Passport'),
    ('ID','Identity card'),
    ('OT','Others')]

    dtype= models.CharField(choices=DOC_TYPES, max_length=2)
    doc_number = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.dtype