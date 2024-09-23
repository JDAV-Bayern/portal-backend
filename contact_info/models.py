from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class Country(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name


class Locality(models.Model):
    postal_code = models.CharField(_('Postal Code'), max_length=10)
    name = models.CharField(_('Name'), max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'))
    is_admin_provided = models.BooleanField(_('Is Admin Provided'), default=False)

    class Meta:
        unique_together = ['postal_code', 'name', 'country']
        verbose_name = _('Locality')
        verbose_name_plural = _('Localities')

    def __str__(self):
        return self.postal_code + ' ' + self.name


class Address(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, verbose_name=_('Contact'))
    line1 = models.CharField(_('Line 1'), max_length=255)
    line2 = models.CharField(_('Line 2'), max_length=255, blank=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, verbose_name=_('Locality'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.line1 + ', ' + str(self.locality)


class BankAccount(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='bank_account', verbose_name=_('Contact'))
    iban = models.CharField(_("IBAN"), max_length=34, unique=True)
    bic = models.CharField(_("BIC"), max_length=11)

    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')

    def __str__(self):
        return self.iban
