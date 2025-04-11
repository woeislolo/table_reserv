from django.db import models
from django.core.validators import MinValueValidator


class Table(models.Model):

    LOCATION_CHOICE = {
        '1': 'зал у окна',
        '2': 'основной зал',
        '3': 'терраса',
    }

    name = models.CharField(max_length=10,
                            null=False,
                            blank=False,
                            verbose_name='Наименование столика')
    seats = models.PositiveSmallIntegerField(null=False,
                                             blank=False,
                                             verbose_name='Кол-во мест')
    location = models.CharField(max_length=20,
                                choices=LOCATION_CHOICE, 
                                blank=False,
                                verbose_name='Расположение')
    
    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики' 
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'
    
    
class Reservation(models.Model):
    customer_name = models.CharField(max_length=50,
                                     null=False,
                                     blank=False,
                                     verbose_name='Имя клиента')
    table_id = models.ForeignKey(Table, 
                                 null=False,
                                 blank=False,
                                 on_delete=models.PROTECT,
                                 related_name='reservations',
                                 verbose_name='Номер столика')
    reservation_time= models.DateTimeField(null=False,
                                           blank=False,
                                           verbose_name='На какое время забронировано')
    duration_minutes = models.PositiveSmallIntegerField(null=False,
                                                        blank=False,
                                                        validators=[MinValueValidator(1, 
                                                                                      "Значение не должно быть меньше 1")],
                                                        verbose_name='Время пребывания, мин')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони' 
        ordering = ('id',)

    def __str__(self):
        return f'Клиент {self.customer_name}, {self.table_id}, {self.reservation_time}, {self.duration_minutes}'
