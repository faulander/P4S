 from .models import Settings

def site_settings(request):
    return {'site_settings': Settings.load()}

# checked for V 0.2.0