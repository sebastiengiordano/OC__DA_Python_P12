from django.db import models


EVENT_STATUS = (
    ('To_Sign', 'To_Sign'),
    ('In_Progress', 'In_Progress'),
    ('Completed', 'Completed'),
)


class Event(models.Model):
    '''This class aims to defined a event.'''

    client = models.ForeignKey(
                            'clients.Client',
                            on_delete=models.CASCADE,
                            related_name='client_event')
    technician = models.ForeignKey(
                            'users.Technician',
                            on_delete=models.CASCADE,
                            related_name='technician_event')
    contract = models.OneToOneField(
                            'contracts.Contract',
                            on_delete=models.CASCADE,
                            related_name='contract_event')
    status = models.CharField(
        verbose_name='contract_title',
        choices=EVENT_STATUS,
        max_length=11,
        default='To_Sign')
    attendees = models.IntegerField(
        verbose_name='attendees')
    event_date = models.DateField()
    note = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['technician']

    def __str__(self):
        return (
            "Event"
            f"\n\tContract title: {self.contract.title}"
            f"\n\tstatus: {self.status}")
