from django.db import models
from django.utils.translation import gettext_lazy as _


class Federation(models.Model):
    NATIONAL = 0
    STATE = 1
    DISTRICT = 2
    TYPE_CHOICES = {
        NATIONAL: _('National Federation'),
        STATE: _('State Federation'),
        DISTRICT: _('District Federation'),
    }

    type = models.IntegerField(_('Level'), choices=TYPE_CHOICES)
    name = models.CharField(_('Name'), max_length=200)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name=_('Parent'), null=True, blank=True)

    def __str__(self):
        return self.TYPE_CHOICES[self.type] + ' ' + self.name
    
    class Meta:
        ordering = ['type', 'name']
        verbose_name = _('Federation')
        verbose_name_plural = _('Federations')

class Section(models.Model):
    number = models.IntegerField(_('Number'), unique=True)
    name = models.CharField(_('Name'), max_length=200)
    state = models.ForeignKey(Federation, on_delete=models.PROTECT, related_name='state_section_set', verbose_name=_('State Federation'))
    district = models.ForeignKey(Federation, on_delete=models.PROTECT, related_name='district_section_set', verbose_name=_('District Federation'), null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')
