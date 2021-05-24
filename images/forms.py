from django import forms

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """Create a form for uploading an image."""

    class Meta:
        model = Image
        fields = ("title", "url", "description")
        widgets = {
            "url": forms.HiddenInput
        }
