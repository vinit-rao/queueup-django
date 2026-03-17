from .models import JoinRequest

def notifications(request):
    if request.user.is_authenticated:
        pending_host_requests = JoinRequest.objects.filter(post__author=request.user, status='Pending').count()
        accepted_applications = JoinRequest.objects.filter(applicant=request.user, status='Accepted').count()
        return {
            'pending_host_requests': pending_host_requests,
            'accepted_applications': accepted_applications,
        }
    return {}