from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _, gettext_noop  # NoQA
from pretix.base.models import Event, Item
from pretix.base.services.cart import CartError
from pretix.base.settings import settings_hierarkey
from pretix.base.signals import validate_cart
from pretix.control.signals import nav_event_settings


@receiver(nav_event_settings, dispatch_uid='pretix_obligatory_item_nav_event_settings')
def nav_event_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(request.organizer, request.event, 'can_change_event_settings',
                                             request=request):
        return []
    return [{
        'label': _('Obligatory Item Purchase'),
        'url': reverse('plugins:pretix_obligatory_item:settings', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_obligatory_item',
    }]


@receiver(validate_cart, dispatch_uid="pretix_obligatory_item_validate_cart")
def validate_cart(sender: Event, positions, **kwargs):
    for item in Item.objects.filter(pk__in=sender.settings.get('obligatory_item_items', [])):
        if not positions.filter(item=item).exists():
            raise CartError(
                _('You need to add the following items to your cart in order to proceed to checkout: {item}').format(
                    item=item
                )
            )


settings_hierarkey.add_default('obligatory_item_items', None, list)
