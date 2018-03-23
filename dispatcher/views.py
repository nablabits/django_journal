from django.shortcuts import render

def dispatcher(request):
    """Get everywhere in the site."""

    return render(request, 'dispatcher/index.html')
