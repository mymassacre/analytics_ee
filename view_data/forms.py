from django.forms import ModelForm

from transfer_files_to_model.models import ReportRuskVolumeCheck


class ReportRuskVolumeCheckForm(ModelForm):
    class Meta:
        model = ReportRuskVolumeCheck
        fields = (
            'Define_subdivision',
        )
