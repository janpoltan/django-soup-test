from django.db import models

class Professional(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    website = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    professional = models.ForeignKey(Professional, related_name='contacts')
    contact_type = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=45)

    def __str__(self):
        return '{0} - {1}'.format(self.contact_type, self.contact_number)
