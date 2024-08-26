from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.forms import formset_factory
from django.core.paginator import Paginator
from .forms import LoginForm, ChildModelForm, GuardianModelForm
from .models import ChildModel,GuardianModel


def index(request):
    return render(request, 'LCHIS/index.html')

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
    ChildFormSet = formset_factory(ChildModelForm)
    GuardianFormSet = formset_factory(GuardianModelForm, extra=0 ,min_num=1)
    
    arguments = {
        'current_user': request.user.username.capitalize(),
        'child_form_set': ChildFormSet(prefix='child'),
        'guardian_form_set': GuardianFormSet(prefix='guardian'),
    }

    if request.method == 'POST':
        child_form_set = ChildFormSet(request.POST, request.FILES, prefix='child')
        guardian_form_set = GuardianFormSet(request.POST, request.FILES, prefix='guardian')
        print(guardian_form_set.is_valid())
        
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
