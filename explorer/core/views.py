from django.shortcuts import render


def welcome(request):
    return render(request, "core/welcome.html")


def legal_notice(request):
    return render(request, "core/legal_notice.html")


def privacy(request):
    return render(request, "core/privacy.html")


def accessibility(request):
    return render(request, "core/accessibility.html")


def contact(request):
    return render(request, "core/contact.html")


def terms(request):
    return render(request, "core/terms.html")
