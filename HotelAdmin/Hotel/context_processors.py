from .models import Tech

def user_info(request):
    if request.user.is_authenticated:
        
        user_profile = Tech.objects.filter(user=request.user).first()
        return {
            'user_name': request.user.username,
            'user': user_profile  
        }
    return {}
