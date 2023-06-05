from typing import Any, Dict
from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget



class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ["username", "password", "email", "full_name", "address",'confirm_password']

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")
        
              
            
        return uname
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Customer with this email already exists.")
        
              
            
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            print(password)
            print(confirm_password)
            raise forms.ValidationError(
            "Password and password confirmation does not match"
            )
        return cleaned_data


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
             'class': 'input100',
             'placeholder':'Please enter username'
    }
              
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
             'class': 'input100',
             'placeholder':'Your Password'
    }
              
    ))


class AdminProductCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminProductCreateForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['color'].required = True
        self.fields['color'].error_messages.update({
            'required': 'Please select at least one data!'})

    class Meta:
        model = Product
        fields = ['is_active','title','main_category','category','instock','color','size','marked_price','selling_price', 'discount_pct','brand',
                  'description','return_policy','is_featured','length','width','height','weight','return_policy','image1','image2','image3','image4','image5']

        
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
                'id' :"one-ecom-product-status",
                'placeholder': 'Product Name',
                'name':"one-ecom-product-published"
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Name'
            }),
            # 'product_id': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Product Id'
            # }),
            'main_category': forms.Select(attrs={
                  'class': 'form-control ',

            }),
            'category': forms.SelectMultiple(attrs={
             'class': 'form-control multipleselect ',
                'data-placeholder': '  Select category ',
                }),
            
          
            'brand': forms.Select(attrs={
                'class': 'form-control',
                # 'id':'example-select',
                # 'name':'example-select',
                #  'data-placeholder': '  Select brands ',
            }),
          
            'length': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'width': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'height': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'weight': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
            'return_policy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Policy incase of Return',
            }),
            'description': SummernoteWidget(),
            'return_policy': SummernoteWidget(),
            'color': forms.SelectMultiple(attrs={
                
             'class': 'form-control multipleselect ',
                'data-placeholder': '  Select color',
                }),
            'size':forms.SelectMultiple(attrs={
             'class': 'form-control multipleselect ',
                'data-placeholder': '  Select size',
                }),
            'marked_price':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter the price'
            }),
            'selling_price':forms.NumberInput(attrs={
                'class':'form-control',
                
            }),
            'discount_pct':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Enter the price'
            }),
            'is_featured':'',
            'instock':forms.TextInput(attrs={
                'class':'form-control',
            }),
             'image1': forms.ClearableFileInput(),
              'image2': forms.ClearableFileInput(),
               'image3': forms.ClearableFileInput(),
                'image4': forms.ClearableFileInput(),
                 'image5': forms.ClearableFileInput(),
            

        }



class AdminProductCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['title','image']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category Name'
            }),
           

            'image': forms.ClearableFileInput(),
            

        }


class AdminProductBrandCreateForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['title','image',]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand Name'
            }),
           
            'image': forms.ClearableFileInput(),
            

        }



class AdminProductColorCreateForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['title','hex_code']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
           
            'hex_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hex code'
            }),
            

        }

class AdminProductSizeCreateForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['title','standard']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }),
           
            'standard': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Size'
            }),
            

        }


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['image1','image2','image3','title']
        # exclude = ()
        widgets = {
            'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control  font-weight-bold text-dark ',
                'style': "border: 1px solid gray;",

            }),'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control  font-weight-bold text-dark ' ,
                'style': "border: 1px solid gray;",

            }),'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control  font-weight-bold text-dark ',
                'style': "border: 1px solid gray;",

            }),         

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
                'placeholder': 'Enter slider title'
            }),


        }


class OrganizationForm(forms.ModelForm):
    
    class Meta:
        model = Organization
        fields = "__all__"
        exclude = ('vat_pan',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                 'style': 'border: 1px solid gray;',
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),

            'contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
            'alt_contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
            'map_location': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'pattern': '[\w\.-]+@[\w\.-]+\.\w{2,4}',
                'style': 'border: 1px solid gray;',

            }),
            'alt_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
            'slogan': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
            'facebook': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
            'instagram': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),
           
            'youtube': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),

            
            'profile_image' : forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'border: 1px solid gray;',
            }),

            'terms_and_conditions': SummernoteWidget(),
            'introduction': SummernoteWidget(),
            'style': 'border: 1px solid gray;',

            
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "mobile", "email"]


class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter the email used in customer account..."
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError(
                "Customer with this account does not exists..")
        return e

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password    