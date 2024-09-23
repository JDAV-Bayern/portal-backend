from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact_info'
    verbose_name = _('Contact Information')
