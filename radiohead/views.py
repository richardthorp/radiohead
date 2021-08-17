from django.shortcuts import render


def handle_404_error(request, exception):
    return render(request, '404_page.html')


def handle_500_error(request, exception=None):
    return render(request, '500_page.html')