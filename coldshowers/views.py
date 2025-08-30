from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ColdShowerLog
from .forms import ColdShowerLogForm

# Create your views here.

class ColdShowerLogListView(LoginRequiredMixin, ListView):
    model = ColdShowerLog
    template_name = "coldshowers/coldshower_list.html"
    context_object_name = "logs"

    def get_queryset(self):
        # Show only logs of the logged-in user
        return ColdShowerLog.objects.filter(user=self.request.user).order_by('-date')

class ColdShowerLogCreateView(LoginRequiredMixin, CreateView):
    model = ColdShowerLog
    form_class = ColdShowerLogForm
    template_name = "coldshowers/coldshower_form.html"
    success_url = reverse_lazy("coldshower_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ColdShowerLogDetailView(LoginRequiredMixin, DetailView):
    model = ColdShowerLog
    template_name = "coldshowers/coldshower_detail.html"
    context_object_name = "log"

class ColdShowerLogUpdateView(LoginRequiredMixin, UpdateView):
    model = ColdShowerLog
    form_class = ColdShowerLogForm
    template_name = "coldshowers/coldshower_form.html"
    success_url = reverse_lazy("coldshower_list")

    def get_queryset(self):
        # Ensure users can only update their own logs
        return ColdShowerLog.objects.filter(user=self.request.user)

class ColdShowerLogDeleteView(LoginRequiredMixin, DeleteView):
    model = ColdShowerLog
    template_name = "coldshowers/coldshower_confirm_delete.html"
    success_url = reverse_lazy("coldshower_list")

    def get_queryset(self):
        # Ensure users can only delete their own logs
        return ColdShowerLog.objects.filter(user=self.request.user)



