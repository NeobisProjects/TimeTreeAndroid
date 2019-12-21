CONFUSED = 1
ACCEPTED = 2
REJECTED = 3

from django.utils.translation import ugettext_lazy as _

choices = (
    (CONFUSED, _('Confused')),
    (ACCEPTED, _('Accepted')),
    (REJECTED, _('Rejected'))
)
