from django.shortcuts import render


def index(request):
    # TODO: implement view function
    context = {}
    return render(request, 'meetandeat/dashboard.html', context)
