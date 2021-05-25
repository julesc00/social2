from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from urllib import request

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

    def save(self, force_insert=False, force_commit=False, commit=True):
        """Override save in order to retrieve the given image and save it."""

        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"

        # Download image from the given URL.
        res = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(res.read()), save=False)

        if commit:
            image.save()
        return image
