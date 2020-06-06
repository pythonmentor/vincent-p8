from django.shortcuts import render


def index(request):
    text = None
    headerImg = None
    context = {'text': text, 'header': headerImg}
    return render(request, 'pages/index.html', context)


def legals(request):
    title = 'Mentions Légales'
    headerImg = 'header_legals.jpg'
    context = {'title': title, 'headerImg': headerImg}
    return render(request, 'pages/legals.html', context)
