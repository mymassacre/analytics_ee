# from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from transfer_files_to_model.models import ReportRuskVolumeCheck
from view_data.forms import ReportRuskVolumeCheckForm


class PaginatedListView(ListView, FormMixin):
    model = ReportRuskVolumeCheck
    form_class = ReportRuskVolumeCheckForm
    template_name = 'view_data/view_data.html'
    paginate_by = 1000

    # def dispatch(self, request, *args, **kwargs):
    #     super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super(PaginatedListView, self).get_queryset()
        queryset = queryset.filter(Define_subdivision="Бийское")[0:2000]
        return queryset

    def post(self, request, *args, **kwargs):
        self.fostatus_form = StatusForm(self.request.POST or None)
        if self.status_form.is_valid():
            define_subdivision = self.request.POST['Define_subdivision']
        else:
            define_subdivision = None
        print(self.request.POST)
        return define_subdivision

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ReportRuskVolumeCheck._meta.fields
        context['Define_subdivision_list'] = (
            set(ReportRuskVolumeCheck.objects.values_list("Define_subdivision", flat=True)))
        context['Define_period_list'] = (
            set(ReportRuskVolumeCheck.objects.values_list("Define_period", flat=True)))
        context['Client_office_list'] = (
            set(ReportRuskVolumeCheck.objects.values_list("Client_office", flat=True)))
        context['Controller_list'] = (
            set(ReportRuskVolumeCheck.objects.values_list("Controller", flat=True)))
        context['data_list'] = ReportRuskVolumeCheck.objects.all()

        return context
