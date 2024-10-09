from django.db import models
from django.utils.translation import gettext_lazy as _


class Reimbursement(models.Model):
    class Type(models.TextChoices):
        COURSE = "course", _("Course")
        COMMITTEE = "committee", _("Committee")

    type = models.CharField(_('Type'), max_length=16, choices=Type)
    participant = models.ForeignKey('people.Person', on_delete=models.PROTECT, verbose_name=_('Participant'))
    note = models.TextField(_('Note'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    def __str__(self) -> str:
        return _("%(type)s reimbursement for %(participant)s at %(created_at)s") % {
            'type': self.Type(self.type).label,
            'participant': self.participant,
            'created_at': self.created_at
        }

    class Meta:
        verbose_name = _('Reimbursement')
        verbose_name_plural = _('Reimbursements')


class CourseDetails(models.Model):
    reimbursement = models.OneToOneField(Reimbursement, on_delete=models.CASCADE, related_name='course_details', verbose_name=_('Reimbursement'))
    course = models.ForeignKey('courses.Course', on_delete=models.PROTECT, verbose_name=_('Course'), null=True, blank=True)

    def __str__(self) -> str:
        return _("Course details for %(reimbursement)s") % {'reimbursement': self.reimbursement}

    class Meta:
        verbose_name = _('Course Reimbursement')
        verbose_name_plural = _('Course Reimbursements')


class TravelDetails(models.Model):
    reimbursement = models.OneToOneField(Reimbursement, on_delete=models.CASCADE, related_name='travel_details', verbose_name=_('Reimbursement'))
    purpose = models.CharField(_('Purpose'), max_length=255)
    location = models.CharField(_('Location'), max_length=255)
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))

    def __str__(self) -> str:
        return _("Travel details for %(reimbursement)s") % {'reimbursement': self.reimbursement}

    class Meta:
        verbose_name = _('Travel Details')
        verbose_name_plural = _('Travel Details')
