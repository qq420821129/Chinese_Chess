from django.shortcuts import render

# Create your views here.


def play(request):
    user = request.user

    return render(request, 'chess.html')
