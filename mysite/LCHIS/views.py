from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model

from .forms import LoginForm, ChildModelForm, GuardianModelForm, GalleryModelForm, VitaminModelForm, AboutUsModelForm, ContactUsModelForm
from .models import ChildModel, GuardianModel, GalleryModel, VitaminModel, AboutUsModel, ContactUsModel
import os

def index(request):
    return redirect(home)


@login_required(login_url='/login')
def user_dashboard(request):
    child_id = request.user.child_id
    child = ChildModel.objects.get(pk=child_id)
    gallery = GalleryModel.objects.all()
    vitamins = VitaminModel.objects.all()
    on_left_abouts = AboutUsModel.objects.filter(on_left = True)
    on_right_abouts = AboutUsModel.objects.filter(on_left = False)
    child_count = ChildModel.objects.count()
    five_old_child_count = ChildModel.objects.filter(years_old=5).count()
    two_old_child_count = ChildModel.objects.filter(years_old=2).count()
    one_old_child_count = ChildModel.objects.filter(years_old__lte=1).count()
    vitamin_count = VitaminModel.objects.filter(quantity__gt=0).count()
    not_available_vitamin_count = VitaminModel.objects.filter(quantity__lt=1).count()
    
    contacts = ContactUsModel.objects.all()
    arguments = {
        'current_user': request.user.first_name.capitalize,
        'child':child,
        'gallery': gallery,
        'vitamins': vitamins,
        'on_left_abouts': on_left_abouts,
        'on_right_abouts': on_right_abouts,
        'child_count': child_count,
        'vitamin_count': vitamin_count,
        'five_old_child_count': five_old_child_count,
        'two_old_child_count': two_old_child_count,
        'one_old_child_count': one_old_child_count,
        'contacts': contacts,
        'not_available_vitamin_count': not_available_vitamin_count,
    }
    return render(request, 'LCHIS/user/home.html', arguments)


def user_registration(request):
    
    child_form = ChildModelForm()
    guardian_form = GuardianModelForm()
    
    arguments = {
        'current_user': request.user.username.capitalize(),
        'child_form': child_form,
        'guardian_form': guardian_form,
    }
    
    if request.method == 'POST':
        child_form = ChildModelForm(request.POST, request.FILES)
        guardian_form = GuardianModelForm(request.POST)
        User = get_user_model()
      
        if child_form.is_valid() and guardian_form.is_valid():
            child = child_form.save()
            # guardian = guardian_form.save(commit=False)
            # guardian.child = child
            # guardian.save()
            guardian = User.objects.create_user(
                username=guardian_form.cleaned_data['username'],
                password=guardian_form.cleaned_data['password'],
                first_name=guardian_form.cleaned_data['first_name'],
                middle_name=guardian_form.cleaned_data['middle_name'],
                last_name=guardian_form.cleaned_data['last_name'],
                child=child
            )
            guardian.save()

            return redirect(login_view)
        else:
            arguments['child_form'] = child_form
            arguments['guardian_form'] = guardian_form
            return render(request, 'LCHIS/pages/registration.html', arguments)
    else:
        return render(request, 'LCHIS/pages/registration.html', arguments)


def home(request):
    child_count = ChildModel.objects.count()
    zero_to_one_old_child = ChildModel.objects.filter(years_old__lt=1).count()
    one_to_six_old_child = ChildModel.objects.filter(Q(years_old__gte=1) & Q(years_old__lte=6)).count()
    six_to_nine_old_child = ChildModel.objects.filter(Q(years_old__gte=6) & Q(years_old__lte=9)).count()
    nine_to_twelve_old_child = ChildModel.objects.filter(Q(years_old__gte=9) & Q(years_old__lte=12)).count()
    
    vitamin_count = VitaminModel.objects.filter(quantity__gt=0).count()
    arguments = {
        'child_count': child_count,
        'zero_to_one_old_child': zero_to_one_old_child,
        'one_to_six_old_child': one_to_six_old_child,
        'six_to_nine_old_child': six_to_nine_old_child,
        'nine_to_twelve_old_child': nine_to_twelve_old_child,
        'vitamin_count': vitamin_count,
    }
    return render(request, 'LCHIS/pages/home.html', arguments)

def gallery(request):
    gallery = GalleryModel.objects.all()
    contacts = ContactUsModel.objects.all()
    arguments = {
        'gallery': gallery,
        'contacts': contacts,
    }
    return render(request, 'LCHIS/pages/gallery.html', arguments)

def vitamins(request):
    vitamins = VitaminModel.objects.all()
    arguments = {
        'vitamins': vitamins,
    }
    return render(request, 'LCHIS/pages/vitamins.html', arguments)

def about_us(request):
    on_left_abouts = AboutUsModel.objects.filter(on_left = True)
    on_right_abouts = AboutUsModel.objects.filter(on_left = False)
    arguments = {
        'on_left_abouts': on_left_abouts,
        'on_right_abouts': on_right_abouts,
    }
    return render(request, 'LCHIS/pages/about_us.html', arguments)

def contact_us(request):
    contacts = ContactUsModel.objects.all()
    arguments = {
        'contacts': contacts,
    }
    return render(request, 'LCHIS/pages/contact_us.html', arguments)

def child_info(request):
    child_id = request.user.child_id
    child = ChildModel.objects.get(pk=child_id)
    arguments = {
        'child':child,
    }
    return render(request, 'LCHIS/pages/child_info.html', arguments)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect(child_list)
            elif user is not None:
                login(request, user)
                return redirect(home)
            else:
                form = LoginForm(request.POST)
                arguments = {
                        'form': form,
                        'error': 'Invalid username or password'
                    }
                return render(request, 'LCHIS/component/login.html', arguments)
    else:
        form = LoginForm()
        arguments = {
            'form': form
        }
    return render(request, 'LCHIS/component/login.html', arguments)

def logout_view(request):
    logout(request)
    return redirect(index)

@permission_required('is_superuser', login_url = '/admin/login')
@login_required(login_url = '/admin/login')
def admin_dashboard(request):
    arguments = {
        'current_user': request.user.username.capitalize,
    }
    return render(request, 'LCHIS/admin/child_list.html', arguments)

@login_required(login_url = '/admin/login')
def child_list(request):
    query = request.GET.get('q')
    
    if query:
        children = ChildModel.objects.filter(Q(child_first_name__icontains=query) | Q(child_middle_name__icontains=query) | Q(child_last_name__icontains=query) ).all()
    else:
        children = ChildModel.objects.all()
    
    if request.method == 'POST':
        selected_images = request.POST.getlist('child_to_delete') 
        if selected_images:
            for pk in selected_images:
                child = ChildModel.objects.get(pk=pk)
                guardian = GuardianModel.objects.get(child=child.pk)
                child.delete()
                guardian.delete()
                
    paginator = Paginator(children, 10)
    page_number = request.GET.get('page')
    if page_number:
        page_obj = paginator.get_page(page_number)
        
    else:
        page_obj = paginator.get_page(1)
    
    arguments = {
        'current_user': request.user.username.capitalize,
        'children': children,
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'LCHIS/admin/child_list.html', arguments)

@login_required(login_url='/admin/login')
def child_detail(request, pk = None, delete_image = None):
    
    child_form = ChildModelForm()
    guardian_form = GuardianModelForm()
    
    arguments = {
        'current_user': request.user.username.capitalize(),
        'child_form': child_form,
        'guardian_form': guardian_form,
    }
    
    
    if pk:
        child = ChildModel.objects.get(pk=pk) 
        guardian = GuardianModel.objects.get(child=child)
        arguments['child_form'] = ChildModelForm(instance=child)
        arguments['child'] = child
        arguments['guardian_form'] = GuardianModelForm(instance=guardian)
        if request.method == 'POST':
            child_form = ChildModelForm(request.POST, request.FILES, instance=child)
            guardian_form = GuardianModelForm(request.POST, instance=guardian)
            if child_form.is_valid() and guardian_form.is_valid():
                
                # print(guardian_form.cleaned_data['first_name'])
                update_guardian = GuardianModel.objects.get(child=child)
                print(update_guardian.first_name)
                update_guardian.username=guardian_form.cleaned_data['username']
                update_guardian.password=guardian_form.cleaned_data['password']
                update_guardian.first_name=guardian_form.cleaned_data['first_name']
                update_guardian.middle_name=guardian_form.cleaned_data['middle_name']
                update_guardian.last_name=guardian_form.cleaned_data['last_name']
                update_guardian.child=child
                update_guardian.save()
                child_form.save()
                # guardian_ = guardian_form.save(commit=False)
                # guardian_.child = child
                # guardian_.save()
                return redirect(child_list)
    
    if pk and delete_image:
        child = ChildModel.objects.get(pk=pk)
        child.delete_image()
        return redirect(child_detail, pk=pk)
    
    if request.method == 'POST':
        child_form = ChildModelForm(request.POST, request.FILES)
        guardian_form = GuardianModelForm(request.POST)
        User = get_user_model()
        
        saveAndAddAnother = int(request.POST['saveAndAdd']) 
        saveAndEditAnother = int(request.POST['saveAndEdit']) 
        if saveAndAddAnother:
            if child_form.is_valid() and guardian_form.is_valid():
                child = child_form.save()
                guardian = User.objects.create_user(
                    username=guardian_form.cleaned_data['username'],
                    password=guardian_form.cleaned_data['password'],
                    first_name=guardian_form.cleaned_data['first_name'],
                    middle_name=guardian_form.cleaned_data['middle_name'],
                    last_name=guardian_form.cleaned_data['last_name'],
                    child=child
                )
                guardian.save()

                return redirect(child_detail)
            
        if saveAndEditAnother:
            if child_form.is_valid() and guardian_form.is_valid():
                child = child_form.save()
                guardian = User.objects.create_user(
                    username=guardian_form.cleaned_data['username'],
                    password=guardian_form.cleaned_data['password'],
                    first_name=guardian_form.cleaned_data['first_name'],
                    middle_name=guardian_form.cleaned_data['middle_name'],
                    last_name=guardian_form.cleaned_data['last_name'],
                    child=child
                )
                guardian.save()

                return redirect(child_detail, pk=child.pk)
            
        
        if child_form.is_valid() and guardian_form.is_valid():
            child = child_form.save()
            # guardian = guardian_form.save(commit=False)
            # guardian.child = child
            # guardian.save()
            guardian = User.objects.create_user(
                username=guardian_form.cleaned_data['username'],
                password=guardian_form.cleaned_data['password'],
                first_name=guardian_form.cleaned_data['first_name'],
                middle_name=guardian_form.cleaned_data['middle_name'],
                last_name=guardian_form.cleaned_data['last_name'],
                child=child
            )
            guardian.save()

            return redirect('child_list')
        else:

            arguments['child_form'] = child_form
            arguments['guardian_form'] = guardian_form
            return render(request, 'LCHIS/admin/child_detail.html', arguments)
    else:
        return render(request, 'LCHIS/admin/child_detail.html', arguments)

@login_required(login_url='/admin/login')
def gallery_list(request):
    query = request.GET.get('q')
    
    if query:
        gallery_list = GalleryModel.objects.filter(Q(type__icontains=query) | Q(date__icontains=query)).all()
    else:
        gallery_list = GalleryModel.objects.all()
    
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
        'page_obj':page_obj,
        'query': query
    }
    return render(request, 'LCHIS/admin/gallery_list.html', arguments)

@login_required(login_url='/admin/login')
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

@login_required(login_url='/admin/login')
def vitamin_list(request):
    query = request.GET.get('q')
    
    if query:
        vitamin_list = VitaminModel.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).all()
    else:
        vitamin_list = VitaminModel.objects.all()
    
    # item = VitaminModel.objects.get(pk=22)
    # item.delete()
    if request.method == 'POST':
        selected_images = request.POST.getlist('image_to_delete') 
        if selected_images:
            for pk in selected_images:
                item = VitaminModel.objects.get(pk=pk)
                item.delete()
    paginator = Paginator(vitamin_list, 10)
    page_number = request.GET.get('page')
    if page_number:
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = paginator.get_page(1)
    
    arguments = {
        'current_user': request.user.username.capitalize,
        'page_obj':page_obj,
        'query': query
    }
    return render(request, 'LCHIS/admin/vitamin_list.html', arguments)

@login_required(login_url='/admin/login')
def vitamin_detail(request, pk=0):
    form = VitaminModelForm
    arguments = {
        'current_user': request.user.username.capitalize,
        'form': form
    }

    if pk != 0:
        item = VitaminModel.objects.get(pk=pk)
        arguments['form'] = VitaminModelForm(instance=item)
        arguments['vitamin'] = item
        if request.method == 'POST':
            confirmDelete = int(request.POST['confirmDelete']) 
            if (confirmDelete):
                item.delete()
                return redirect(vitamin_list)
            form = VitaminModelForm(request.POST, request.FILES, instance=item)
            if request.FILES:
                path = item.image.path
                os.remove(path)
            if form.is_valid():
                form.save()
                return redirect(vitamin_list)
        
    if request.method == 'POST' and pk == 0:
        vitamin_form = VitaminModelForm(request.POST, request.FILES)
        saveAndAddAnother = int(request.POST['saveAndAdd']) 
        saveAndEditAnother = int(request.POST['saveAndEdit']) 

        if vitamin_form.is_valid():
            vitaminInstance = vitamin_form.save()
            if (saveAndAddAnother ==1):
                print('saveAndAddAnother')
                return redirect(vitamin_detail)
            elif(saveAndEditAnother==1):
                arguments['form'] = vitamin_form

                print('saveAndEditAnother')

                return redirect(vitamin_detail, pk=vitaminInstance.pk)
            else:
                return redirect(vitamin_list)
        else:
            arguments['form'] = vitamin_form

    return render(request, 'LCHIS/admin/vitamin_detail.html', arguments)

@login_required(login_url='/admin/login')
def about_us_list(request):
    query = request.GET.get('q')
    
    if query:
        about_us_list_list = AboutUsModel.objects.filter(Q(header__icontains=query) | Q(description__icontains=query)).all()
    else:
        about_us_list_list = AboutUsModel.objects.all()
        
    if request.method == 'POST':
        selected_items = request.POST.getlist('item_to_delete') 
        if selected_items:
            for pk in selected_items:
                item = AboutUsModel.objects.get(pk=pk)
                item.delete()
    paginator = Paginator(about_us_list_list, 10)
    page_number = request.GET.get('page')
    if page_number:
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = paginator.get_page(1)
    
    arguments = {
        'current_user': request.user.username.capitalize,
        'page_obj':page_obj,
        'query':query
    }
    return render(request, 'LCHIS/admin/about_us_list.html', arguments)

@login_required(login_url='/admin/login')
def about_us_detail(request, pk=0):
    form = AboutUsModelForm
    arguments = {
        'current_user': request.user.username.capitalize,
        'form': form
    }

    if pk != 0:
        item = AboutUsModel.objects.get(pk=pk)
        arguments['form'] = AboutUsModelForm(instance=item)
        arguments['vitamin'] = item
        if request.method == 'POST':
            confirmDelete = int(request.POST['confirmDelete']) 

            if (confirmDelete):
                item.delete()
                return redirect(about_us_list)
            form = AboutUsModelForm(request.POST, request.FILES, instance=item)
            if request.FILES:
                path = item.image.path
                os.remove(path)
            if form.is_valid():
                form.save()
                return redirect(about_us_list)
        
    if request.method == 'POST' and pk == 0:
        about_us_form = AboutUsModelForm(request.POST, request.FILES)
        saveAndAddAnother = int(request.POST['saveAndAdd']) 
        saveAndEditAnother = int(request.POST['saveAndEdit']) 

        if about_us_form.is_valid():
            vitaminInstance = about_us_form.save()
            if (saveAndAddAnother ==1):
                print('saveAndAddAnother')
                return redirect(about_us_detail)
            elif(saveAndEditAnother==1):
                arguments['form'] = about_us_form

                print('saveAndEditAnother')

                return redirect(about_us_detail, pk=vitaminInstance.pk)
            else:
                return redirect(about_us_list)
        else:
            arguments['form'] = about_us_form

    return render(request, 'LCHIS/admin/about_us_detail.html', arguments)

@login_required(login_url='/admin/login')
def contact_us_list(request):
    query = request.GET.get('q')
    
    if query:
        contact_us_list_list = ContactUsModel.objects.filter(Q(header__icontains=query) | Q(description__icontains=query)).all()
    else:
        contact_us_list_list = ContactUsModel.objects.all()

    if request.method == 'POST':
        selected_items = request.POST.getlist('item_to_delete') 
        if selected_items:
            for pk in selected_items:
                item = AboutUsModel.objects.get(pk=pk)
                item.delete()
    paginator = Paginator(contact_us_list_list, 10)
    page_number = request.GET.get('page')
    if page_number:
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = paginator.get_page(1)
    
    arguments = {
        'current_user': request.user.username.capitalize,
        'page_obj':page_obj,
        'query': query
    }
    return render(request, 'LCHIS/admin/contact_us_list.html', arguments)

@login_required(login_url='/admin/login')
def contact_us_detail(request, pk=0):
    form = ContactUsModelForm
    arguments = {
        'current_user': request.user.username.capitalize,
        'form': form
    }

    if pk != 0:
        item = ContactUsModel.objects.get(pk=pk)
        arguments['form'] = ContactUsModelForm(instance=item)
        arguments['vitamin'] = item
        if request.method == 'POST':
            confirmDelete = int(request.POST['confirmDelete']) 
            if (confirmDelete):
                item.delete()
                return redirect(contact_us_list)
            form = ContactUsModelForm(request.POST, request.FILES, instance=item)
            if request.FILES:
                path = item.image.path
                os.remove(path)
            if form.is_valid():
                form.save()
                return redirect(contact_us_list)
        
    if request.method == 'POST' and pk == 0:
        contact_us_form = ContactUsModelForm(request.POST, request.FILES)
        saveAndAddAnother = int(request.POST['saveAndAdd']) 
        saveAndEditAnother = int(request.POST['saveAndEdit']) 

        if contact_us_form.is_valid():
            vitaminInstance = contact_us_form.save()
            if (saveAndAddAnother ==1):
                print('saveAndAddAnother')
                return redirect(contact_us_detail)
            elif(saveAndEditAnother==1):
                arguments['form'] = contact_us_form

                print('saveAndEditAnother')

                return redirect(contact_us_detail, pk=vitaminInstance.pk)
            else:
                return redirect(contact_us_list)
        else:
            arguments['form'] = contact_us_form

    return render(request, 'LCHIS/admin/contact_us_detail.html', arguments)