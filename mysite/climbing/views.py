from django.shortcuts import render

# Create your views here.

def test(request):
    print("asd")
    return render(request, 'base.html',{'items':"items"})
