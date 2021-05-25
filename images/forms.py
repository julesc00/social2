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

    def clean_url(self):
        """Verify only jpeg, jpg or png extensions are allowed."""

        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.split(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL doesn't match valid image extensions.")
        return url
