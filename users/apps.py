from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class ApplicantsConfig(AppConfig):
    name = 'users'
    verbose_name = _('Applicants')

    def ready(self):
        import users.signals
