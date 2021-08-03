from django import forms
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _, gettext_noop  # NoQA
from pretix.base.forms import SettingsForm
from pretix.base.models import Event, Item
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin


class ObligatoryItemSettingsForm(SettingsForm):
    obligatory_item_items = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'scrolling-multiple-choice'}
        ),
        label=_('Obligatory items'),
        required=False,
        queryset=Item.objects.none(),
        initial=None
    )

    def __init__(self, *args, **kwargs):
        event = kwargs['obj']
        super().__init__(*args, **kwargs)

        self.fields['obligatory_item_items'].queryset = event.items.all()

    def clean(self):
        data = super().clean()

        for k, v in self.fields.items():
            if isinstance(v, forms.ModelMultipleChoiceField):
                answstr = [o.pk for o in data[k]]
                data[k] = answstr

        return data


class ObligatoryItemSettings(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = ObligatoryItemSettingsForm
    template_name = 'pretix_obligatory_item/settings.html'
    permission = 'can_change_settings'

    def get_success_url(self) -> str:
        return reverse('plugins:pretix_obligatory_item:settings', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug
        })
