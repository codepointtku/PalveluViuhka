from django.conf import settings

def export_vars(request):
    data = {}
    data['DEBUG'] = getattr(settings, "DEBUG", "")
    data['FORCE_SCRIPT_NAME'] = getattr(settings, "FORCE_SCRIPT_NAME", "")
    return data
