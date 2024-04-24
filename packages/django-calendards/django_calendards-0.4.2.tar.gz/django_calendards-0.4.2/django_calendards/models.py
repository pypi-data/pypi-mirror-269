from django.db import models


class Calendar(models.Model):
    modal_title = models.CharField('calendar_name', default="휴진안내", help_text=r"줄넘기기 : \n", max_length=40)
    activate = models.BooleanField(default=False, help_text="활성창 1개만 가능")

    def __str__(self):
        return self.modal_title


class Event(models.Model):
    title = models.CharField('title', default="휴진", max_length=20)
    date_of_event = models.DateField()
    calendar = models.ForeignKey(
        'Calendar',
        related_name='calendar',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return str(self.title) + '/' + str(self.date_of_event)
