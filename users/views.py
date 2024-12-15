from django.shortcuts import redirect
from django.contrib import messages
from app import render, is_post
from app.views import update_view
from app.auth import login_required, officials_only
from .forms import UserForm, ProfilePictureForm

# Create your views here.
@login_required
def change_picture(request):
    if is_post(request):
        form = ProfilePictureForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid() and form.save():
            messages.success(request, 'Profile picture updated successfully')
            return redirect(request.user.profile)

    else: form = ProfilePictureForm(instance=request.user)
        
    return render(
        request,'users/change-picture',
        title='Update Profile Picture',
        form = form
    )

@officials_only()
def update_name(request):
    return update_view(
        request,
        instance=request.user,
        form_class=UserForm,
        form_header='Update name',
    )