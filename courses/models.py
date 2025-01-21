from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseYear(models.Model):
    year = models.IntegerField(_('Year'), unique=True)

    def __str__(self):
        return str(self.year)
    
    class Meta:
        ordering = ['-year']
        verbose_name = _('Course Year')
        verbose_name_plural = _('Course Years')


class Course(models.Model):
    BASIC = 'GA'
    CONTINUING = 'FB'
    ADVANCED = 'AM'
    ASSEMBLY = 'JV'
    SPECIAL = 'SV'
    TYPE_CHOICES = {
        BASIC: _('Basic Training'),
        CONTINUING: _('Continuing Training'),
        ADVANCED: _('Advanced Training'),
        ASSEMBLY: _('Youth Assembly'),
        SPECIAL: _('Special Event'),
    }

    number = models.CharField(_('Course Number'), max_length=10, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=255)
    type = models.CharField(_('Course Type'), max_length=255, choices=TYPE_CHOICES)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    location = models.CharField(_('Location'), max_length=255)
    year = models.ForeignKey(CourseYear, on_delete=models.PROTECT, verbose_name=_('Course Year'))
    federation = models.ForeignKey('sections.Federation', on_delete=models.PROTECT, verbose_name=_('Federation'))

    def __str__(self):
        return (self.number + ' ' if self.number else '') + self.name
    
    class Meta:
        ordering = ['federation', '-end_date', '-number']
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


# class CourseInformation(models.Model):
#     federation = models.OneToOneField(Course, on_delete=models.CASCADE, primary_key=True, verbose_name=_('Course'))
#     
#     class Meta:
#         verbose_name = _('Course Information')
#         verbose_name_plural = _('Course Information')
