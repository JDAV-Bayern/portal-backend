from django.db import models
from django.utils.translation import gettext_lazy as _

from contact_info.models import Contact


class Person(Contact):
    given_name = models.CharField(_('Given Name'), max_length=255)
    family_name = models.CharField(_('Family Name'), max_length=255)
    section = models.ForeignKey('sections.Section', on_delete=models.SET_NULL, verbose_name=_('Section'), null=True)
    email = models.EmailField(_('Email'))

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __str__(self):
        return self.given_name + ' ' + self.family_name
