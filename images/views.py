from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm


@login_required
def image_create_view(request):
    """Save a new image object."""
    if request.method == "POST":
        # Form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # Assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image added successfully")

            # Redirect to new created item detail view.
            return redirect(new_item.get_absolute_url())

    else:
        # Build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    context = {"form": form}
    return render(request, "images/image/create.html", context)
