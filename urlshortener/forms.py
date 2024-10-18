'''
Shortener Forms urlshortener/forms.py
'''

from django import forms

from .models import ShortenedURL

# import gettext lazy translation
from django.utils.translation import gettext_lazy as _

class ShortenerForm(forms.ModelForm):
    
    long_url = forms.URLField(
        label=_('Your URL to shorten'),
        widget=forms.URLInput(
            attrs={
                'placeholder': _('Enter a URL to shorten'),
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = ShortenedURL

        fields = ('long_url',)
