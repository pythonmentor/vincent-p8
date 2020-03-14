from django.shortcuts import render
from django.contrib.auth import logout

@login_required(login_url='/accounts/login/')
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = 'Profil'
        headerImg = 'header_contact.jpg'
        context = {'title': title, 'headerImg': headerImg}
        return render(request, 'account/index.html', context)
