from django.shortcuts import render


def error404(request):
    if '/play/' in request.path:
        return render(request, 'play_404.html', {'play_404': True},  status=404)
    else:
        return render(request, '404.html', status=404)
