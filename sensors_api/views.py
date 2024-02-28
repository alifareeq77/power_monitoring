from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import UserDashboard


@login_required
def user_dashboard(request):
    user = request.user
    try:
        user_dashboard = UserDashboard.objects.get(user=user)
        context = {'dashboard_link': user_dashboard.dashboard_link}
        return render(request, 'sensors_api/user_dashboard.html', context)
    except UserDashboard.DoesNotExist:
        return HttpResponseNotFound('<h1>Dashboard link not found</h1>')
