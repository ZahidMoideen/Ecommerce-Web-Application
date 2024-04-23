# forms.py
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'image', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Product Title'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product Description'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Upload Product Image'}),
            'priority': forms.NumberInput(attrs={'placeholder': 'Product Priority'}),
        }
