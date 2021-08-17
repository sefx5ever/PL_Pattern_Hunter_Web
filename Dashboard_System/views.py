from django.shortcuts import render

# Create your views here.
def account_setting(request):
    context = {'dashboardUser' : 'dashboard_user.html'}
    return render(request,'account_setting.html',context)

def dashboard_user(request):
    return render(request,'dashboard_user.html')

# def testapi(request):
#     return HttpResponse('Hello World!')

# class ShareDataViewSet(viewsets.ModelViewSet):
#     queryset = Share_History.objects.all()
#     serializer_class = ShareDataSerializer
