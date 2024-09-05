from django import forms
from .models import ChildModel, GuardianModel, GalleryModel
from django.forms.widgets import FileInput, TextInput, Textarea, Select

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                              label='Password')
    
class ChildModelForm(forms.ModelForm):
    class Meta:
      model=ChildModel
      fields = ['first_name', 'middle_name', 'last_name', 'birthdate', 'years_old', 'months_old', 'gender', 'image']
      
    first_name = forms.CharField(label='First Name',
                                 error_messages={'required': 'Please enter first name.'},
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label='Middle Name',
                                  error_messages={'required': 'Please enter middle name.'},
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',
                                error_messages={'required': 'Please enter Last name.'},
                                widget  =forms.TextInput(attrs={'class': 'form-control'}))
    birthdate = forms.CharField(label='Birthdate',
                                error_messages={'required':'Birthdate is required'},
                                widget=forms.TextInput(attrs={'class': 'form-control birthdate', 'autocomplete': 'off'}))
    years_old = forms.IntegerField(label='Year',
                             widget=forms.NumberInput(attrs={'class': 'form-control','readonly':'True'}),
                              required=False)
    months_old = forms.IntegerField(label='Month',
                             widget=forms.NumberInput(attrs={'class': 'form-control','readonly':'True'}),
                              required=False)
    gender = forms.ChoiceField(label='Gender',
                               choices=(('M', 'M'),('F', 'F')),
                               widget=forms.Select(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)

 
class GuardianModelForm(forms.ModelForm):
    class Meta:
      model=GuardianModel
      fields = ['first_name', 'middle_name', 'last_name', ]
      
    first_name = forms.CharField(label='First Name',
                                 error_messages={'required': 'Please enter guardian first name.'},
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label='Middle Name',
                                  error_messages={'required': 'Please enter middle name.'},
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',
                                error_messages={'required': 'Please enter Last name.'},
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
# TODO add gallery form
class GalleryModelForm(forms.ModelForm):
  class Meta:
    model = GalleryModel
    fields = '__all__'
    widgets = {
          'image': FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
          'type': Select(attrs={'class': 'custom-select'}),
          'date': TextInput( attrs={'class': 'form-control date', 'autocomplete': 'off'})
        }
