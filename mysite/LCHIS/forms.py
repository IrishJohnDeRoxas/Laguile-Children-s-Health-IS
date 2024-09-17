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
        'barangay':TextInput( attrs={'class':'form-control', 'required':''}),
        'name_of_bhw':TextInput( attrs={'class':'form-control', 'required':''}),
        'purok':TextInput( attrs={'class':'form-control', 'required':''}),
        'nurse':TextInput( attrs={'class':'form-control', 'required':''}),
        
        'first_name':TextInput( attrs={'class':'form-control', 'required':''}),
        'middle_name':TextInput( attrs={'class':'form-control', 'required':''}),
        'last_name':TextInput( attrs={'class':'form-control', 'required':''}),
        'birthdate':TextInput( attrs={'class':'form-control', 'required':''}),
        'image':FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
        'years_old':TextInput( attrs={'class':'form-control', 'required':'', 'readonly':'true'}),
        'months_old':TextInput( attrs={'class':'form-control', 'required':'', 'readonly':'true'}),
        'gender':Select(attrs={'class': 'custom-select'}),
        
        'bcg':TextInput( attrs={'class':'form-control'}),
        'hepa_b':TextInput( attrs={'class':'form-control'}),
        'penta_1':TextInput( attrs={'class':'form-control'}),
        'penta_2':TextInput( attrs={'class':'form-control'}),
        'penta_3':TextInput( attrs={'class':'form-control'}),
        'opv_1':TextInput( attrs={'class':'form-control'}),
        'opv_2':TextInput( attrs={'class':'form-control'}),
        'opv_3':TextInput( attrs={'class':'form-control'}),
        'ipv_1':TextInput( attrs={'class':'form-control'}),
        'ipv_2':TextInput( attrs={'class':'form-control'}),
        'pcv_1':TextInput( attrs={'class':'form-control'}),
        'pcv_2':TextInput( attrs={'class':'form-control'}),
        'pcv_3':TextInput( attrs={'class':'form-control'}),
        'mcv_1':TextInput( attrs={'class':'form-control'}),
        'mcv_2':TextInput( attrs={'class':'form-control'}),
        
        'remarks':TextInput( attrs={'class':'form-control', 'required':''}),
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
      fields = '__all__'
      widgets = {
        'first_name': TextInput( attrs={'class': 'form-control', 'required':''}),
        'middle_name': TextInput( attrs={'class': 'form-control', 'required':''}),
        'last_name': TextInput( attrs={'class': 'form-control', 'required':''}),
      }
 
class GalleryModelForm(forms.ModelForm):
  class Meta:
    model = GalleryModel
    fields = '__all__'
    widgets = {
          'image': FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
          'type': Select(attrs={'class': 'custom-select'}),
          'date': TextInput( attrs={'class': 'form-control date', 'autocomplete': 'off'})
        }
