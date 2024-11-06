# from django.http import HttpResponse, HttpResponseRedirect
# from . import services
from .services import *
from .models import ReportRuskVolumeCheck, ReportSued16010, ReportSued7108
from django.shortcuts import render


source_path = r'C:\Users\korne\Desktop\ПО'
period = define_period('year-month')
report_rusk_volume_check = '0'
report_sued_71_08_check = '0'
report_sued_160_10_check = '0'


def transfer_files_to_model_index(request):
    global source_path, period, report_rusk_volume_check, report_sued_71_08_check, report_sued_160_10_check
    if request.method == 'POST':

        if request.POST["period"] == '':
            period = define_period('year-month')
        else:
            period = request.POST["period"]

        try:
            report_rusk_volume_check = request.POST["report_rusk_volume_check"]
        except KeyError:
            report_rusk_volume_check = 0

        try:
            report_sued_71_08_check = request.POST["report_sued_71_08_check"]
        except KeyError:
            report_sued_71_08_check = 0

        try:
            report_sued_160_10_check = request.POST["report_sued_160_10_check"]
        except KeyError:
            report_sued_160_10_check = 0

    path = source_path + "\\" + period.split("-")[0] + "\\" + period

    if report_rusk_volume_check == '1':
        transfer_files_to_model(ReportRuskVolumeCheck, path + r"\_asuse\Сверка ПО", period)

    if report_sued_71_08_check == '1':
        transfer_files_to_model(ReportSued7108, path + r"\_forsage\71_08", period)

    if report_sued_160_10_check == '1':
        transfer_files_to_model(ReportSued16010, path + r"\_forsage\160_10", period)

    return render(request, 'transfer_files_to_model/transfer_files_to_model.html',
                  {
                      "period": period,
                      "report_rusk_volume_check": report_rusk_volume_check,
                      "report_sued_7108": report_sued_71_08_check,
                      "report_sued_16010": report_sued_160_10_check,
                  })
