from django.shortcuts import render

# Create your views here.
def index(request):
    text = None
    headerImg = None
    context = {'text': text, 'header': headerImg}
    return render(request, 'pages/index.html', context)

def legals(request):
    title = 'Mentions Légales'
    headerImg = 'header_legals.jpg'
    context = {'title': title, 'headerImg': headerImg}
    return render(request, 'pages/content/legals.html', context)

def contact(request):
    title = 'Envoyez-nous un pigeon'
    headerImg = 'header_contact.jpg'
    context = {'title': title, 'headerImg': headerImg}
    return render(request, 'pages/content/contact.html', context)

