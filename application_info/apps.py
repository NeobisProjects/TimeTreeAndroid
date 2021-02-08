from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class ApplicationInfoConfig(AppConfig):
    name = 'application_info'
    verbose_name = _('Application info')
