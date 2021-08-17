from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.http import require_POST
# from .forms import AuthenthicationForm,RegisterForm

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def reset_password(request):
    return render(request,'reset_password.html')

# @require_POST
# def check_account(request):
#     form = AuthenthicationForm(request.POST)
#     print('='*60)
#     print(form.is_valid())
#     if form.is_valid():
#         return HttpResponse(True)
#     else:
#         print(form.errors.get_json_data())
#         return HttpResponse(False)

# @require_POST
# def add_account(request):
#     form = RegisterForm(request.POST)
#     if form.is_valid():
#         user = form.save(commit=False)
#         user.password = form.cleaned_data.get('password')
#         user.save()
#         return HttpResponse('Account sign up successfully!')
#     else:
#         print(form.errors.get_json_data())
#         return HttpResponse('Account sign up fail!')