from django.db import models


class Federation(models.Model):
    NATIONAL = 0
    STATE = 1
    DISTRICT = 2
    TYPE_CHOICES = {
        NATIONAL: 'Bundesverband',
        STATE: 'Landesverband',
        DISTRICT: 'Bezirk',
    }

    type = models.IntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.TYPE_CHOICES[self.type] + ' ' + self.name
    
    class Meta:
        ordering = ['type', 'name']

class Section(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    state = models.ForeignKey(Federation, related_name='state_section_set', on_delete=models.PROTECT)
    district = models.ForeignKey(Federation, related_name='district_section_set', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
