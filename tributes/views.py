from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import AnonymousTributeForm, NewTributeForm, TributeForm
from .models import Tribute


class TributeCreateAnonymousView(CreateView):
    model = Tribute
    form_class = AnonymousTributeForm
    object = None

    def form_valid(self, form):
        site = get_current_site(self.request)
        ip_address = self.request.META.get('REMOTE_ADDR', None)
        self.object = form.save_with_comments(
            user=self.request.user, site_id=site.id, ip_address=ip_address)
        return redirect(self.object.get_absolute_url())


class TributeCreateView(LoginRequiredMixin, CreateView):
    model = Tribute
    form_class = NewTributeForm
    object = None

    def form_valid(self, form):
        site = get_current_site(self.request)
        ip_address = self.request.META.get('REMOTE_ADDR', None)
        self.object = form.save_with_comments(
            user=self.request.user, site_id=site.id, ip_address=ip_address)
        return redirect(self.object.get_absolute_url())

    def get(self, request, *args, **kwargs):
        if self.has_tribute():
            return redirect('tributes:edit')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.has_tribute():
            return redirect('tributes:edit')
        return super().post(request, *args, **kwargs)

    def get_redirect_field_name(self):
        return None

    def has_tribute(self):
        return Tribute.objects.filter(owner=self.request.user).exists()


class TributeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tributes/tribute_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _object = Tribute.objects.filter(owner=self.request.user).first()
        context.update({'object': _object})
        return context

    def get_redirect_field_name(self):
        return None


class TributeDetailView(DetailView):
    def get_queryset(self):
        return Tribute.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # enable comment moderation for owner
        user = self.request.user
        context.update({'is_owner_authenticated': user.username == self.object.owner})

        return context


class TributeHomeView(TemplateView):
    template_name = 'tributes/tribute_home.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tributes:dashboard')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest': Tribute.objects.order_by('-created_at')[:5]
        })
        return context


class TributeShareView(LoginRequiredMixin, DetailView):
    template_name = 'tributes/tribute_share.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Tribute, owner=self.request.user)

    def get_redirect_field_name(self):
        return None


class TributeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TributeForm

    def get_object(self, queryset=None):
        return get_object_or_404(Tribute, owner=self.request.user)

    def get_redirect_field_name(self):
        return None
