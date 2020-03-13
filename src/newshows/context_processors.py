from .models import Settings

def settings(request):
    return {'settings': Settings.load()}

# checked for V 0.2.0