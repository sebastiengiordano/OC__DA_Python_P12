from django.db import models


class Contract(models.Model):
    '''This class aims to defined a contract.'''

    title = models.CharField(
                            verbose_name='contract_title',
                            max_length=200)
    saler = models.ForeignKey(
                            'users.Saler',
                            on_delete=models.CASCADE,
                            related_name='contract_saler')
    client = models.ForeignKey(
                            'clients.Client',
                            on_delete=models.CASCADE,
                            related_name='contract_client')
    amount = models.FloatField(verbose_name='amount')
    payment_due = models.DateField()
    signed = models.BooleanField(
                            null=True,
                            default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['title', 'amount', 'payment_due']

    class Meta:
        unique_together = \
            ('title', 'saler', 'client')

    def __str__(self):
        return (
            f"{self.title}"
            f"\tsaler: {self.saler.id}"
            f"\tclient: {self.client.id}")
