from django.db import models


# Create your models here.
# noinspection PyUnresolvedReferences
class ReportRuskVolumeCheck(models.Model):  # Verbose name должен совпадать с названием столбца в исходном файле
    Client_office = models.CharField(max_length=30, verbose_name="КО")
    Locality = models.CharField(max_length=100, verbose_name="Населённый пункт")
    Controller = models.CharField(max_length=100, null=True, blank=True, verbose_name="Контроллер")
    RUSK_account_number = models.IntegerField(verbose_name="ЛС Lite")
    SUED_account_number = models.IntegerField(verbose_name="ЛС ФОРСАЖ")
    ASUSE_account_number = models.IntegerField(null=True, blank=True, verbose_name="Номер абонента АСУСЭ")
    RUSK_full_name = models.CharField(max_length=100, verbose_name="ФИО АСУСЭ")
    RUSK_address = models.CharField(max_length=200, verbose_name="Адрес")
    SAP_account_number = models.IntegerField(null=True, blank=True, verbose_name="Номер абонента БРИЗ")
    SAP_full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="ФИО БРИЗ")
    Calculation_method = models.CharField(max_length=50, null=True, blank=True, verbose_name="Метод расчета")
    RUSK_volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ПО АСУСЭ")
    SAP_volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="ПО БРИЗ")
    SAP_address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Адрес БРИЗ")
    Difference = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Разность")
    Apartment_building = models.BooleanField(null=True, verbose_name="Есть МОП")
    Rate = models.CharField(max_length=50, null=True, blank=True, verbose_name="Тариф")
    Operating_organization = models.CharField(max_length=200, null=True, blank=True,
                                              verbose_name="Эксплуатирующая организация")
    RUSK_metering_device = models.CharField(max_length=50, null=True, blank=True, verbose_name="ПУ АО")
    SAP_metering_device = models.CharField(max_length=50, null=True, blank=True, verbose_name="ПУ СО")
    Penalty = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                  verbose_name="неустойка по ППРФ354")
    Status_metering_device = models.CharField(max_length=50, null=True, blank=True, verbose_name="Статус ПУ")
    Define_subdivision = models.CharField(max_length=30, verbose_name="ОСП (определенный)")
    Define_period = models.DateField(verbose_name="Расчетный период (определенный)")

    class Meta:
        ordering = [
            "Client_office",
            "Locality",
            "Controller",
            "RUSK_account_number",
            "SUED_account_number",
            "ASUSE_account_number",
            "RUSK_full_name",
            "RUSK_address",
            "SAP_account_number",
            "SAP_full_name",
            "Calculation_method",
            "RUSK_volume",
            "SAP_volume",
            "SAP_address",
            "Difference",
            "Apartment_building",
            "Rate",
            "Operating_organization",
            "RUSK_metering_device",
            "SAP_metering_device",
            "Penalty",
            "Status_metering_device",
            "Define_subdivision",
            "Define_period"
        ]

        db_table = "report_rusk_volume_check"
        verbose_name = "РУСК ФЛ - Сверка ПО"
        verbose_name_plural = "РУСК ФЛ - Сверка ПО"

    def __str__(self):
        return str(self.RUSK_account_number) + ' ' + str(self.Define_period)


class ReportSued16010(models.Model):  # Verbose name должен совпадать с названием столбца в исходном файле
    Client_office = models.CharField(max_length=30, verbose_name="Участок")
    Electric_grid_organization = models.CharField(max_length=100, null=True, blank=True,
                                                  verbose_name="Наименование ТСО")
    FIAS_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Код ФИАС")
    Unique_code_point_of_calculation_public_utility = models.CharField(max_length=50, null=True, blank=True,
                                                                       verbose_name="Уникальный код точки расчета ОДН")
    Name_of_the_management_company = models.CharField(max_length=100, null=True, blank=True,
                                                      verbose_name="Наименование УК/способ управления")
    Unique_house_code = models.IntegerField(verbose_name="Уникальный код дома")
    Period = models.DateField(verbose_name="Расчетный период  в формате YYYY.MM")
    Post_office = models.IntegerField(null=True, blank=True, verbose_name="Отделение связи")
    Locality = models.CharField(max_length=100, null=True, blank=True, verbose_name="Населенный пункт")
    Region = models.CharField(max_length=100, null=True, blank=True, verbose_name="Административный район")
    Street = models.CharField(max_length=100, null=True, blank=True, verbose_name="Улица")
    House = models.CharField(max_length=50, null=True, blank=True, verbose_name="Дом")
    House_type = models.CharField(max_length=100, null=True, blank=True,
                                  verbose_name="Тип дома (2-4 кв, 5-29 кв, от 30-ти квартир)")
    Availability_public_metering_device = models.CharField(max_length=10, null=True, blank=True,
                                                           verbose_name="Наличие ОДПУ")
    Technical_feasibility_of_installing_public_metering_device = models.CharField(max_length=100, null=True, blank=True,
                                                                                  verbose_name="Наличие технической возможности установки ОДПУ")
    Sign_of_contractual_relations = models.IntegerField(null=True, blank=True,
                                                        verbose_name="Признак договорных отношений")
    Who_is_the_public_utility_billed_to = models.CharField(max_length=100, null=True, blank=True,
                                                           verbose_name="Кому выставляется ОДН")
    Principle_of_calculating_public_utility = models.CharField(max_length=50, null=True, blank=True,
                                                               verbose_name="Принцип  расчета ОДН (полностью/в рамках норматива)")
    Calculation_method = models.CharField(max_length=50, null=True, blank=True, verbose_name="Способ расчета")
    Type_of_calculation_public_utility = models.CharField(max_length=50, null=True, blank=True,
                                                          verbose_name="Тип учета на ТП/ Тип расчета ОДН")
    Slab_type = models.CharField(max_length=50, null=True, blank=True, verbose_name="Тип плиты")
    Rate = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                               verbose_name="Величина тарифа на ТП")
    Balance_at_start = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                           verbose_name="Остаток на начало периода")
    Total_expenses_public_metering_device = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                                verbose_name="Суммарный расход по ОДПУ")
    Total_consumption_of_nonresidential_premises_and_transit_consumers = models.DecimalField(max_digits=10,
                                                                                             decimal_places=3,
                                                                                             null=True, blank=True,
                                                                                             verbose_name="Суммарный расход нежилых помещений и транзитных потребителей")
    Total_consumption_of_apartments_with_metering_devices = models.DecimalField(max_digits=10, decimal_places=3,
                                                                                null=True, blank=True,
                                                                                verbose_name="Суммарный расход квартир с ПУ")
    Total_consumption_of_apartments_without_metering_devices = models.DecimalField(max_digits=10, decimal_places=3,
                                                                                   null=True, blank=True,
                                                                                   verbose_name="Суммарный расход квартир без ПУ")
    Total_individual_expenses_for_an_apartment_building = models.DecimalField(max_digits=10, decimal_places=3,
                                                                              null=True, blank=True,
                                                                              verbose_name="Суммарный индивидуальный расход по МКЖД")
    Public_utility_for_apartments = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                        verbose_name="ОДН для квартир")
    Public_utility_for_nonresidential_premises_and_third_party_consumers = models.DecimalField(max_digits=10,
                                                                                               decimal_places=3,
                                                                                               null=True, blank=True,
                                                                                               verbose_name="ОДН для нежилых помещений и сторонних потребителей")
    Total_distributed_public_utility = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                           verbose_name="Суммарный распределенный ОДН по МКЖД")
    Recalculation_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                               verbose_name="Величина перерасчета по ТП кВт.ч")
    Remaining_expense_for_the_current_month = models.DecimalField(max_digits=10, decimal_places=3, null=True,
                                                                  blank=True,
                                                                  verbose_name="Остаток расхода текущего месяца")
    Public_utility_to_standard = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                     verbose_name="ОДН по нормативу")
    Public_utility_above_standard = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                        verbose_name="ОДН сверхнорматив")
    Negative_public_utility_at_the_beginning_of_the_period = models.DecimalField(max_digits=10, decimal_places=3,
                                                                                 null=True, blank=True,
                                                                                 verbose_name="Отрицательный ОДН на начало периода")
    Negative_public_utility_at_the_end_of_the_period = models.DecimalField(max_digits=10, decimal_places=3, null=True,
                                                                           blank=True,
                                                                           verbose_name="Отрицательный ОДН на конец периода")
    Public_utility_by_public_metering_device = models.DecimalField(max_digits=10, decimal_places=3, null=True,
                                                                   blank=True, verbose_name="ОДН по ОДПУ")
    Accounted_for_negative_public_utility = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                                verbose_name="Учтено отрицательного ОДН")
    Public_utility_for_utility_provider = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                              verbose_name="ОДН для Исполнителя услуг")
    Control_method = models.CharField(max_length=50, null=True, blank=True, verbose_name="Способ управления")
    Name_of_utility_provider = models.CharField(max_length=100, null=True, blank=True, verbose_name="Наименование ИКУ")
    Number_of_the_agreement_with_utility_provider = models.CharField(max_length=30, null=True, blank=True,
                                                                     verbose_name="Номер договора с ИКУ")
    Number_of_apartments_with_metering_devices = models.IntegerField(null=True, blank=True,
                                                                     verbose_name="Количество квартир с ИПУ")
    Number_of_apartments_without_metering_devices = models.IntegerField(null=True, blank=True,
                                                                        verbose_name="Количество квартир без  ИПУ")
    Number_of_apartments_with_indications = models.IntegerField(null=True, blank=True,
                                                                verbose_name="Количество квартир с показаниями")
    Number_of_disabled_apartments = models.IntegerField(null=True, blank=True,
                                                        verbose_name="Количество отключенных квартир")
    Method_of_calculating_public_utility = models.CharField(max_length=30, null=True, blank=True,
                                                            verbose_name="Метод начисления ОДН")
    Name_of_the_standard_public_utility = models.CharField(max_length=30, null=True, blank=True,
                                                           verbose_name="Наименование норматива ОДН")
    Number_of_residents = models.IntegerField(null=True, blank=True, verbose_name="Количество проживающих")
    Area_of_common_property = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                                  verbose_name="Площадь общего имущества")
    Total_area_of_residential_and_nonresidential_premises = models.DecimalField(max_digits=10, decimal_places=3,
                                                                                null=True, blank=True,
                                                                                verbose_name="Общая площадь жилых и нежилых помещений")
    Define_subdivision = models.CharField(max_length=30, verbose_name="ОСП (определенный)")
    Define_period = models.DateField(verbose_name="Расчетный период (определенный)")

    class Meta:
        ordering = [
            "Client_office",
            "Electric_grid_organization",
            "FIAS_code",
            "Unique_code_point_of_calculation_public_utility",
            "Name_of_the_management_company",
            "Unique_house_code",
            "Period",
            "Post_office",
            "Locality",
            "Region",
            "Street",
            "House",
            "House_type",
            "Availability_public_metering_device",
            "Technical_feasibility_of_installing_public_metering_device",
            "Sign_of_contractual_relations",
            "Who_is_the_public_utility_billed_to",
            "Principle_of_calculating_public_utility",
            "Calculation_method",
            "Type_of_calculation_public_utility",
            "Slab_type",
            "Rate",
            "Balance_at_start",
            "Total_expenses_public_metering_device",
            "Total_consumption_of_nonresidential_premises_and_transit_consumers",
            "Total_consumption_of_apartments_with_metering_devices",
            "Total_consumption_of_apartments_without_metering_devices",
            "Total_individual_expenses_for_an_apartment_building",
            "Public_utility_for_apartments",
            "Public_utility_for_nonresidential_premises_and_third_party_consumers",
            "Total_distributed_public_utility",
            "Recalculation_amount",
            "Remaining_expense_for_the_current_month",
            "Public_utility_to_standard",
            "Public_utility_above_standard",
            "Negative_public_utility_at_the_beginning_of_the_period",
            "Negative_public_utility_at_the_end_of_the_period",
            "Public_utility_by_public_metering_device",
            "Accounted_for_negative_public_utility",
            "Public_utility_for_utility_provider",
            "Control_method",
            "Name_of_utility_provider",
            "Number_of_the_agreement_with_utility_provider",
            "Number_of_apartments_with_metering_devices",
            "Number_of_apartments_without_metering_devices",
            "Number_of_apartments_with_indications",
            "Number_of_disabled_apartments",
            "Method_of_calculating_public_utility",
            "Name_of_the_standard_public_utility",
            "Number_of_residents",
            "Area_of_common_property",
            "Total_area_of_residential_and_nonresidential_premises",
            "Define_subdivision",
            "Define_period"
        ]

        db_table = "report_sued_160_10"
        verbose_name = "СУЭД - 160.10"
        verbose_name_plural = "СУЭД - 160.10"


class ReportSued7108(models.Model):  # Verbose name должен совпадать с названием столбца в исходном файле
    SUED_account_number = models.IntegerField(verbose_name="3.1. 10 значный номер лицевого счета")
    SUED_volume = models.DecimalField(max_digits=10, decimal_places=2,
                                      verbose_name="Отгружено \"Д\" 20. кВт.ч (ст.22.1+ст.23.1+ст.24.1+ст.25.1) кВтч.")
    Define_subdivision = models.CharField(max_length=30, verbose_name="ОСП (определенный)")
    Define_period = models.DateField(verbose_name="Расчетный период (определенный)")

    class Meta:
        ordering = [
            "SUED_account_number",
            "SUED_volume",
            "Define_subdivision",
            "Define_period"
        ]

        db_table = "report_sued_71_08"
        verbose_name = "СУЭД - 71.08"
        verbose_name_plural = "СУЭД - 71.08"
