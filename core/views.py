from django.shortcuts import render


def home_view(request):
    if request.user.is_authenticated:
        # Show dashboard/logged-in home
        return render(request, 'base.html')
    else:
        # Show landing page for guests
        return render(request, 'landing.html')
