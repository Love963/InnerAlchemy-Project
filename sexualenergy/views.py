from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SexualEnergySession, SexualEnergyLog
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
@login_required
def energy_dashboard(request):
    sessions = SexualEnergySession.objects.filter(user=request.user).order_by('-created_at')
    logs = SexualEnergyLog.objects.filter(user=request.user).order_by('-logged_at')
    context = {
        'sessions': sessions,
        'logs': logs,
    }
    return render(request, 'sexualenergy/dashboard.html', context)


# Sexual Energy Session Views
class SexualEnergySessionListView(LoginRequiredMixin, ListView):
    model = SexualEnergySession
    template_name = "sexualenergy/session_list.html"
    context_object_name = "sessions"

    def get_queryset(self):
        return SexualEnergySession.objects.filter(user=self.request.user)


class SexualEnergySessionDetailView(LoginRequiredMixin, DetailView):
    model = SexualEnergySession
    template_name = "sexualenergy/session_detail.html"
    context_object_name = "session"


class SexualEnergySessionCreateView(LoginRequiredMixin, CreateView):
    model = SexualEnergySession
    fields = ["intention", "practice_notes", "duration_minutes"]
    template_name = "sexualenergy/session_form.html"
    success_url = reverse_lazy("sexualenergy:session_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SexualEnergySessionUpdateView(LoginRequiredMixin, UpdateView):
    model = SexualEnergySession
    fields = ["intention", "practice_notes", "duration_minutes"]
    template_name = "sexualenergy/session_form.html"
    success_url = reverse_lazy("sexualenergy:session_list")


class SexualEnergySessionDeleteView(LoginRequiredMixin, DeleteView):
    model = SexualEnergySession
    template_name = "sexualenergy/session_confirm_delete.html"
    success_url = reverse_lazy("sexualenergy:session_list")

# Sexual Energy Log Views
class SexualEnergyLogListView(LoginRequiredMixin, ListView):
    model = SexualEnergyLog
    template_name = "sexualenergy/log_list.html"
    context_object_name = "logs"

    def get_queryset(self):
        return SexualEnergyLog.objects.filter(user=self.request.user)


class SexualEnergyLogDetailView(LoginRequiredMixin, DetailView):
    model = SexualEnergyLog
    template_name = "sexualenergy/log_detail.html"
    context_object_name = "log"


class SexualEnergyLogCreateView(LoginRequiredMixin, CreateView):
    model = SexualEnergyLog
    fields = ["urges_felt", "energy_level", "redirect_activity", "reflection"]
    template_name = "sexualenergy/log_form.html"
    success_url = reverse_lazy("sexualenergy:log_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SexualEnergyLogUpdateView(LoginRequiredMixin, UpdateView):
    model = SexualEnergyLog
    fields = ["urges_felt", "energy_level", "redirect_activity", "reflection"]
    template_name = "sexualenergy/log_form.html"
    success_url = reverse_lazy("sexualenergy:log_list")


class SexualEnergyLogDeleteView(LoginRequiredMixin, DeleteView):
    model = SexualEnergyLog
    template_name = "sexualenergy/log_confirm_delete.html"
    success_url = reverse_lazy("sexualenergy:log_list")




    