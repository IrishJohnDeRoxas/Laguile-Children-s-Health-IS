from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.forms import formset_factory
from django.core.paginator import Paginator
from .forms import LoginForm, ChildModelForm, GuardianModelForm, GalleryModelForm
from .models import ChildModel,GuardianModel, GalleryModel
import os


def index(request):
    gallery_list = GalleryModel.objects.all()
    arguments = {
        'current_user': request.user.username.capitalize,
        'gallery_list': gallery_list
    }

    return render(request, 'LCHIS/index.html', arguments)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username = username, password = password)
            
            if user is not None and user.is_superuser:
                login( request, user )

                return redirect(admin_dashboard)
            else:
                form = LoginForm(request.POST)
                arguments = {
                        'form': form,
                        'error': 'Invalid username or password'
                    }
                return render(request, 'LCHIS/login.html', arguments)
    else:
        form = LoginForm()
        arguments = {
            'form': form
        }
    return render(request, 'LCHIS/login.html', arguments)

def logout_view(request):
    logout(request)
    return redirect(index)

@login_required(login_url = '/login/')
def admin_dashboard(request):
    arguments = {
        'current_user': request.user.username.capitalize,
    }
    return render(request, 'LCHIS/admin/dashboard.html', arguments)

@login_required(login_url = '/login/')
def child_list(request):
    guardians = GuardianModel.objects.prefetch_related(
        Prefetch('children', queryset=ChildModel.objects.all())
    )
    # ChildModel.objects.all().delete()
    # guardians.delete()
    paginator = Paginator(guardians, 10)
    page_number = request.GET.get('page')
    if page_number:
        page_obj = paginator.get_page(page_number)
        
    else:
        page_obj = paginator.get_page(1)
    
    arguments = {
        'current_user': request.user.username.capitalize,
        'guardians': guardians,
        'page_obj': page_obj
    }
    return render(request, 'LCHIS/admin/child_list.html', arguments)

@login_required(login_url='/login/')
def child_detail(request, child_id = None):
    # TODO Add child info
    # TODO Populate form when clicked on 
    ChildFormSet = formset_factory(ChildModelForm, extra=0 ,min_num=1)
    GuardianFormSet = formset_factory(GuardianModelForm, extra=0 ,min_num=1)
    
    arguments = {
        'current_user': request.user.username.capitalize(),
        'child_form_set': ChildFormSet(prefix='child'),
        'guardian_form_set': GuardianFormSet(prefix='guardian'),
    }

    if request.method == 'POST':
        child_form_set = ChildFormSet(request.POST, request.FILES, prefix='child')
        guardian_form_set = GuardianFormSet(request.POST, request.FILES, prefix='guardian')
        print(guardian_form_set.errors)
        
        if child_form_set.is_valid() and guardian_form_set.is_valid():
            
            for guardian_form in guardian_form_set:
                guardian_instance = guardian_form.save()
                
            for child_form in child_form_set:
                child_instance = child_form.save()   
                guardian_instance.children.add(child_instance)  
                     
    
            arguments['message'] = 'success'
            return redirect(child_list)
        else:
            arguments['child_form_set'] = child_form_set
            arguments['guardian_form_set'] = guardian_form_set
            arguments['error'] = 'Invalid form data'
            return render(request, 'LCHIS/admin/child_detail.html', arguments)
    else:
        return render(request, 'LCHIS/admin/child_detail.html', arguments)

@login_required(login_url='/login/')
def gallery_list(request):
    gallery_list = GalleryModel.objects.all()
    
    # item = GalleryModel.objects.get(pk=22)
    # item.delete()
    if request.method == 'POST':
        selected_images = request.POST.getlist('image_to_delete') 
        if selected_images:
            for pk in selected_images:
                item = GalleryModel.objects.get(pk=pk)
                item.delete()
    paginator = Paginator(gallery_list, 10)
    page_number = request.GET.get('page')
    if page_number:
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = paginator.get_page(1)
    
    arguments = {
        'current_user': request.user.username.capitalize,
        'page_obj':page_obj
    }
    return render(request, 'LCHIS/admin/gallery_list.html', arguments)

@login_required(login_url='/login/')
def gallery_detail(request, pk=0):
    form = GalleryModelForm
    arguments = {
        'current_user': request.user.username.capitalize,
        'form': form
    }

    if pk != 0:
        item = GalleryModel.objects.get(pk=pk)
        arguments['form'] = GalleryModelForm(instance=item)
        arguments['gallery'] = item
        if request.method == 'POST':
            confirmDelete = int(request.POST['confirmDelete']) 
            if (confirmDelete):
                item.delete()
                return redirect(gallery_list)
            form = GalleryModelForm(request.POST, request.FILES, instance=item)
            if request.FILES:
                path = item.image.path
                os.remove(path)
            if form.is_valid():
                form.save()
                return redirect(gallery_list)
        
    if request.method == 'POST' and pk == 0:
        gallery_form = GalleryModelForm(request.POST, request.FILES)
        saveAndAddAnother = int(request.POST['saveAndAdd']) 
        saveAndEditAnother = int(request.POST['saveAndEdit']) 

        if gallery_form.is_valid():
            galleryInstance = gallery_form.save()
            if (saveAndAddAnother ==1):
                print('saveAndAddAnother')
                return redirect(gallery_detail)
            elif(saveAndEditAnother==1):
                arguments['form'] = gallery_form

                print('saveAndEditAnother')

                return redirect(gallery_detail, pk=galleryInstance.pk)
            else:
                return redirect(gallery_list)
        else:
            arguments['form'] = gallery_form


        
    return render(request, 'LCHIS/admin/gallery_detail.html', arguments)