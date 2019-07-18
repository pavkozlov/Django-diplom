from django.shortcuts import render


# Create your views here.
def mainpage(request):
    context = dict()
    return render(request, 'shop/index.html', context=context)
