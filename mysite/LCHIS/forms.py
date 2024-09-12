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
      fields = '__all__'
      widgets = {
        'barangay':TextInput( attrs={'class':'form-control'}),
        'name_of_bhw':TextInput( attrs={'class':'form-control'}),
        'purok':TextInput( attrs={'class':'form-control'}),
        'nurse':TextInput( attrs={'class':'form-control'}),
        
        'first_name':TextInput( attrs={'class':'form-control'}),
        'middle_name':TextInput( attrs={'class':'form-control'}),
        'last_name':TextInput( attrs={'class':'form-control'}),
        'birthdate':TextInput( attrs={'class':'form-control'}),
        'image':FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
        'years_old':TextInput( attrs={'class':'form-control', 'readonly':'true'}),
        'months_old':TextInput( attrs={'class':'form-control', 'readonly':'true'}),
        'gender':Select(attrs={'class': 'custom-select'}),
        }
      error_messages = {
      'first_name': {
          'required': 'Please enter a first name.',
          'invalid': 'First name must be a valid string.',
          # Add more custom error messages here as needed
        }
      }
      labels = {
        'barangay':'Barangay:',
        'nurse':'Name of Widwife/Nurse:',
        'name_of_bhw':'Name of BHW:',
        'purok':'Purok:',
        'months_old':'Months\'s',
        'years_old':'Year\'s',
      }
      

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
    
class GalleryModelForm(forms.ModelForm):
  class Meta:
    model = GalleryModel
    fields = '__all__'
    widgets = {
          'image': FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
          'type': Select(attrs={'class': 'custom-select'}),
          'date': TextInput( attrs={'class': 'form-control date', 'autocomplete': 'off'})
        }
