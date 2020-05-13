from django.shortcuts import redirect


def HomePage(request):
    return redirect('account:login')