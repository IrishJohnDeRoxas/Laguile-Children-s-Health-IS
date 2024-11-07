from django import forms
from .models import ChildModel, GuardianModel, GalleryModel, VitaminModel, AboutUsModel
from django.forms.widgets import FileInput, TextInput, Textarea, Select, CheckboxInput, NumberInput

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
        
        'child_first_name':TextInput( attrs={'class':'form-control', 'required':''}),
        'child_middle_name':TextInput( attrs={'class':'form-control', 'required':''}),
        'child_last_name':TextInput( attrs={'class':'form-control', 'required':''}),
        'birthdate':TextInput( attrs={'class':'form-control', 'required':'', 'autocomplete': 'off'}),
        'image':FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
        
        'height':TextInput( attrs={'class':'form-control', 'required':''}),
        'weight':TextInput( attrs={'class':'form-control', 'required':''}),
        'condition':Textarea( attrs={'class':'form-control', 'required':''}),
        'years_old':TextInput( attrs={'class':'form-control', 'required':'', 'readonly':'true'}),
        'months_old':TextInput( attrs={'class':'form-control', 'required':'', 'readonly':'true'}),
        'gender':Select(attrs={'class': 'custom-select'}),
        
        'name_of_mother':TextInput( attrs={'class':'form-control'}),
        'mother_history':Textarea( attrs={'class':'form-control'}),
        'name_of_father':TextInput( attrs={'class':'form-control'}),
        'father_history':Textarea( attrs={'class':'form-control'}),
        
        'bcg':TextInput( attrs={'class':'form-control date-picker'}),
        'hepa_b':TextInput( attrs={'class':'form-control date-picker'}),
        'penta_1':TextInput( attrs={'class':'form-control date-picker'}),
        'penta_2':TextInput( attrs={'class':'form-control date-picker'}),
        'penta_3':TextInput( attrs={'class':'form-control date-picker'}),
        'opv_1':TextInput( attrs={'class':'form-control date-picker'}),
        'opv_2':TextInput( attrs={'class':'form-control date-picker'}),
        'opv_3':TextInput( attrs={'class':'form-control date-picker'}),
        'ipv_1':TextInput( attrs={'class':'form-control date-picker'}),
        'ipv_2':TextInput( attrs={'class':'form-control date-picker'}),
        'pcv_1':TextInput( attrs={'class':'form-control date-picker'}),
        'pcv_2':TextInput( attrs={'class':'form-control date-picker'}),
        'pcv_3':TextInput( attrs={'class':'form-control date-picker'}),
        'mcv_1':TextInput( attrs={'class':'form-control date-picker'}),
        'mcv_2':TextInput( attrs={'class':'form-control date-picker'}),
        
        'remarks':TextInput( attrs={'class':'form-control', 'required':''}),
        }
      labels = {
        'barangay':'Barangay:',
        'child_first_name':'First name',
        'child_middle_name':'Middle name',
        'child_last_name':'Last name',
        'nurse':'Name of Midwife/Nurse:',
        'name_of_bhw':'Name of BHW:',
        'purok':'Purok:',
        'months_old':'Months',
        'years_old':'Years',
      }     

class GuardianModelForm(forms.ModelForm):
    class Meta:
      model=GuardianModel
      fields = '__all__'
      widgets = {
        'first_name': TextInput( attrs={'class': 'form-control', 'required':''}),
        'middle_name': TextInput( attrs={'class': 'form-control', 'required':''}),
        'last_name': TextInput( attrs={'class': 'form-control', 'required':''}),
        'username': TextInput( attrs={'class': 'form-control', 'required':''}),
        'password': TextInput( attrs={'class': 'form-control', 'required':''}),
      }

class GalleryModelForm(forms.ModelForm):
  class Meta:
    model = GalleryModel
    fields = '__all__'
    widgets = {
          'image': FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput'}),
          'type': Select(attrs={'class': 'custom-select', 'required':''}),
          'date': TextInput( attrs={'class': 'form-control date', 'required':'', 'autocomplete': 'off'})
        }
    
class VitaminModelForm(forms.ModelForm):
  class Meta:
    model = VitaminModel
    fields = '__all__'
    widgets = {
          'image': FileInput(attrs={'class': 'custom-file-input', 'id':'imageInput',}),
          'name': TextInput( attrs={'class': 'form-control', 'required':''}),
          'description':Textarea( attrs={'class':'form-control', 'required':''}),
          'quantity':NumberInput( attrs={'class':'form-control', 'required':''}),
        }
    
class AboutUsModelForm(forms.ModelForm):
  class Meta:
    model = AboutUsModel
    fields = '__all__'
    widgets = {
          'header': TextInput( attrs={'class': 'form-control', 'required':''}),
          'description': Textarea( attrs={'class': 'form-control', 'required':''}),
        }
