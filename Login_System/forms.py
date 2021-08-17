from django import forms
# from API.models import Account

# class AuthenthicationForm(forms.ModelForm):
#     user = forms.CharField(max_length=20)
#     password = forms.CharField(max_length=20)

#     def clean(self):
#         user_ = self.cleaned_data.get('user')
#         password_ = self.cleaned_data.get('password')
#         isExists = Account.objects.filter(user=user_,password=password_).exists()
#         if not isExists:
#             raise forms.ValidationError(message='Username is exist!')
#         return user_
    
#     class Meta: 
#         model = Account
#         fields = "__all__"
#         error_messages = {
#             'user' : { 'invalid' : 'Invalid Username!' },
#             'password' : { 'invalid' : 'Invalid Username!' }
#         }

# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(max_length=20,min_length=6)
#     re_password = forms.CharField(max_length=20,min_length=6)

#     def clean(self):
#         password = self.cleaned_data.get('password')
#         re_password = self.cleaned_data.get('re_password')
#         if (password != re_password):
#             raise forms.ValidationError('Password and Re-enter Password is not match!')
#         return password

#     class Meta(AuthenthicationForm.Meta):
#         model = Account
#         exclude = ['re_password']