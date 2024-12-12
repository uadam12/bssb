from io import BytesIO
from PIL import Image
from django.shortcuts import render as render_template
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.core.files import File
from crispy_forms.utils import render_crispy_form

def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except:
        return None

def is_post(request):
    return request.method == 'POST'

def is_htmx(request):
    return 'HX-Request' in request.headers

def render(request, template:str, title='Borno State Scholarship Board', *args, **kwargs):
    kwargs.setdefault('title', title)

    if not template.endswith('.html'):
        template = f"{template}.html"
    
    return render_template(request, template, *args, kwargs)

def render_form(request, form):
    ctx = {}
    ctx.update(csrf(request))
    return HttpResponse(render_crispy_form(form, context=ctx))