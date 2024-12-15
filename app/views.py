from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from . import render, is_post, is_htmx

def trigger(response:HttpResponse, event:str):
    response.headers['HX-Trigger'] = event

def htmx_empty_response(data_change):
    response = HttpResponse(status=204)

    if data_change: 
        trigger(response, 'dataChanged')
    
    return response

def data_view(request, data, data_template, title, table_headers=[], add_url=None, main_template='data', filter_form=None):
    if is_htmx(request):
        return render(request, data_template, data=data)

    return render(
        request,main_template, 
        add_url = add_url,
        title=title, data=data, 
        filter_form=filter_form,
        data_template=data_template,
        with_htmx=True, with_modal=True,
        table_headers = table_headers
    )

def create_view(
    request, form_class, success_url, form_header,
    data_change=True, save_instantly=True, submit_text=None,
    success_msg='', further_action=None):

    form = form_class()

    if is_post(request):
        form = form_class(data=request.POST, files=request.FILES)

        if form.is_valid():
            print('Before save')
            model = form.save(save_instantly)
            print('After save')

            if success_msg: messages.success(request, success_msg)
            if further_action is not None:
                res = further_action(model)
                if res: return res
            
            if is_htmx(request):
                return htmx_empty_response(data_change)

            return redirect(success_url)
    
    if is_htmx(request):
        return render(request, 'parts/modal-form', form=form, header=form_header)

    return render(
        request, 'form', form=form, 
        success_url=reverse_lazy(success_url),
        title=form_header, submit_text=submit_text
    )

def update_view(request, form_class, instance, form_header,
    data_change=True, save_instantly=True, further_action=None):

    form = form_class(instance=instance)
    instance_str = str(instance)

    if is_post(request):
        form = form_class(instance=instance, data=request.POST, files=request.FILES)

        if form.is_valid():
            model = form.save(save_instantly)
            
            if further_action:
                res = further_action(model)
                if res: return res
            else: messages.success(request, f"{instance_str} updated successfully.")

            if is_htmx(request):
                return htmx_empty_response(data_change)

            return redirect(instance.list_url)
    
    if is_htmx(request):
        return render(request, 'parts/modal-form', form=form, header=form_header)

    return render(
        request, 'form', form=form, 
        success_url=instance.list_url,
        title=form_header
    )

def delete_view(request, model, header, data_change=True):
    
    if is_post(request):
        model.delete()
        messages.success(request, f"{str(model)} deleted successfully!")
        if is_htmx(request):
            return htmx_empty_response(data_change)
        
        return redirect(model.list_url)
        
    if is_htmx(request):
        return render(request, 'parts/confirmation-modal', model=model, header=header)
    
    return render(request, 'delete', model=model, title=header)