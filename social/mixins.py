from django.core.exceptions import PermissionDenied
from .models import Community

class IsSubscriberMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        if self.request.user in instance.subscribers.all():
            context['is_subscriber'] = True
        else:
            context['is_subscriber'] = False
        return context
    
class IsSubscriberFormsMixin():
    def dispatch(self, request, *args, **kwargs):
        community = Community.objects.filter(pk = self.kwargs['community_pk']).first()
        if self.request.user not in community.subscribers.all():
            return PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)