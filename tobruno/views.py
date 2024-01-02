from django.shortcuts import render


def to_bruno(request):
    return render(request, 'tobruno/home.html')
