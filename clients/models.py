from django.db import models


class Client(models.Model):
    '''This class aims to defined a client.'''

    first_name = models.CharField(
        verbose_name='first name',
        max_length=25)
    last_name = models.CharField(
        verbose_name='last name',
        max_length=25)
    email = models.EmailField(
        verbose_name='email address',
        max_length=50,
        blank=True,
        null=True,)
    phone = models.CharField(
        verbose_name='phone number',
        max_length=15,
        blank=True,
        null=True)
    mobil = models.CharField(
        verbose_name='mobil number',
        max_length=15,
        blank=True,
        null=True)
    company_name = models.CharField(
        verbose_name='company name',
        max_length=100)
    sales_contact = models.ForeignKey(
                            'users.Saler',
                            on_delete=models.CASCADE,
                            related_name='sales_contact')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'company_name']

    class Meta:
        unique_together = \
            ('first_name', 'last_name', 'email', 'phone', 'mobil')

    def __str__(self):
        return (
            f"{self.first_name}"
            f" / {self.last_name}"
            f" - from {self.company_name}")
