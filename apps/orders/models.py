from django.db import models
from apps.core.models import BaseModel
from apps.customer.models import Customer
from apps.users.models import User


class OrderType(BaseModel):
    code = models.CharField(max_length=5, verbose_name="Код типа")
    name = models.CharField(max_length=50, verbose_name="Название типа")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Тип заказа"
        verbose_name_plural = "Типы заказов"


class OrderStatus(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Название статуса")
    code = models.CharField(max_length=10, verbose_name="Код статуса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Заказчик")
    year = models.PositiveSmallIntegerField(verbose_name="Год заказа")
    number = models.PositiveIntegerField(verbose_name="Порядковый номер")
    order_type = models.ForeignKey(OrderType, on_delete=models.PROTECT, verbose_name="Тип заказа")
    part = models.PositiveSmallIntegerField(default=1, verbose_name="Часть заказа")
    suffix = models.CharField(max_length=10, blank=True, verbose_name="Суффикс (ДОП, РЕК и т.д.)")

    month = models.PositiveSmallIntegerField(verbose_name="Месяц заказа")
    production_week = models.PositiveSmallIntegerField(verbose_name="Производственная неделя")
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_orders', verbose_name="Менеджер")
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Масса")
    packages = models.PositiveIntegerField(blank=True, null=True, verbose_name="Количество упаковок")
    start_date = models.DateField(verbose_name="Дата начала обработки")
    technologist = models.ForeignKey(User, on_delete=models.PROTECT, related_name='technologist_orders',
                                     verbose_name="Технолог")
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, verbose_name="Статус")

    # Материалы
    has_mdf = models.BooleanField(default=False, verbose_name="МДФ")
    has_hardware = models.BooleanField(default=False, verbose_name="Фурнитура")
    has_glass = models.BooleanField(default=False, verbose_name="Стекла")
    has_cnc = models.BooleanField(default=False, verbose_name="ЧПУ")

    # Площади материалов
    ldsp_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                    verbose_name="ЛДСП 16-25мм, АГТ (м²)")
    mdf_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="МДФ (м²)")
    edge_04 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                  verbose_name="Кромка 0,4мм (м/п)")
    edge_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                 verbose_name="Кромка 2мм (м/п)")
    edge_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                 verbose_name="Кромка 1мм (м/п)")
    total_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                     verbose_name="Общая площадь (м²)")
    serial_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      verbose_name="Площадь серийной продукции (м²)")
    portal_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      verbose_name="Площадь каминных порталов (м²)")

    complaint_reason = models.TextField(blank=True, verbose_name="Причина рекламации")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    parent_order = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="Родительский заказ")

    @property
    def order_number(self):
        base = f"{self.customer.code}-{str(self.year)[-2:]}-{self.number}{self.order_type.code}"
        if self.part > 1:
            base += f"-{self.part}"
        if self.suffix:
            base += f"-{self.suffix}"
        return base

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        unique_together = ('customer', 'year', 'number', 'order_type', 'part', 'suffix')


class OrderFile(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files', verbose_name="Заказ")
    file = models.FileField(upload_to='order_files/', verbose_name="Файл")
    description = models.CharField(max_length=100, blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.order.order_number} - {self.description}"

    class Meta:
        verbose_name = "Файл заказа"
        verbose_name_plural = "Файлы заказов"
