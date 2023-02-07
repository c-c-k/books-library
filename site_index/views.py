from django.conf import settings
from django.shortcuts import render


# Create your views here.
def index(request):
    user = request.user
    greet_msg = (
        f"Hello {user.username} you are at the Django Testing site index"
        if user.is_authenticated
        else
        "Welcome to the Django Testing site index"
    )
    context = {
        'greet_msg': greet_msg,
        'applications': settings.APPLICATION_URLS,
    }
    return render(
        request=request,
        template_name='site_index/index.html',
        context=context,
    )
