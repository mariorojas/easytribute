from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import NewTributeForm, TributeForm
from .models import Tribute


class TributeLoginRequireMixin(LoginRequiredMixin):
    def get_redirect_field_name(self):
        return None


class TributeCreateView(TributeLoginRequireMixin, CreateView):
    model = Tribute
    form_class = NewTributeForm
    object = None

    def form_valid(self, form):
        site = get_current_site(self.request)
        ip_address = self.request.META.get('REMOTE_ADDR', None)
        self.object = form.save_with_comments(
            user=self.request.user, site_id=site.id, ip_address=ip_address)
        return redirect(self.object.get_absolute_url())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tribute_from_db = Tribute.objects.filter(owner=self.request.user)
            if tribute_from_db.exists():
                return redirect('tributes:edit')
        return super().dispatch(request, *args, **kwargs)


class TributeDetailView(DetailView):
    model = Tribute

    def get_queryset(self):
        return Tribute.objects.filter(active=True)


class TributeHomeView(TemplateView):
    template_name = 'tributes/tribute_home.html'


class TributeUpdateView(TributeLoginRequireMixin, UpdateView):
    model = Tribute
    form_class = TributeForm

    def get_object(self, queryset=None):
        return get_object_or_404(Tribute, owner=self.request.user)
