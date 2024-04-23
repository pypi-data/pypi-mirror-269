from django.core.exceptions import ValidationError
from artd_price_list.models import PriceList
from django import forms
from django.utils.translation import gettext_lazy as _


class PriceListForm(forms.ModelForm):
    class Meta:
        model = PriceList
        fields = "__all__"

    def clean_special_price_from(self):
        special_price_from = self.cleaned_data.get("special_price_from")
        if special_price_from:
            return special_price_from
        else:
            raise ValidationError(_("Start date cannot be empty"))

    def clean_special_price_to(self):
        special_price_to = self.cleaned_data.get("special_price_to")
        if special_price_to:
            special_price_from = self.cleaned_data.get("special_price_from")
            if special_price_from and special_price_to < special_price_from:
                raise ValidationError(
                    _("The end date must be later than the start date")
                )
            return special_price_to
        else:
            raise ValidationError(_("End date cannot be empty"))
