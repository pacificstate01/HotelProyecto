from .models import TipoUsuario

def user_info(request):
    if request.user.is_authenticated:
        
        user_profile = TipoUsuario.objects.filter(username=request.user.username).first()
        return {
            'user_name': request.user.username,
            'user': user_profile  
        }
    return {}
