# forms.py 
from django import forms 
from .models import Product, Part#, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, part):
        return "%s" % part.part_name



class ProductForm(forms.ModelForm): 
    class Meta: 
        model = Product
        fields = ['product_name', 'price_in_pence', 'image', 'parts']

    parts = CustomMMCF(
        queryset=Part.objects.all(),
    widget=forms.CheckboxSelectMultiple
    )



class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ["part_name", "type", "price_in_pence", "link"]
        
'''
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review', 'image1', 'image2']
'''

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=30) # Required
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


