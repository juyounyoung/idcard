import datetime

from django.db import models


# Create your models here.
class Board(models.Model):
    title = models.CharField(db_column='title', max_length=100, null=False)
    school_name = models.CharField(db_column='school_name', max_length=10, null=False)
    reporting_date = models.DateTimeField(db_column='reporting_date', default=datetime.date.today())
    del_yn = models.IntegerField(db_column='del_yn', default=0)

    class Meta:
        managed = False
        db_table = 'board_list'


class Users_user(models.Model):
    school_ID = models.CharField(db_column='school_ID', max_length=10, null=False)
    school_name = models.CharField(db_column='school_name', max_length=10, null=False)
    school_address = models.CharField(db_column='school_address', max_length=10, null=False)
    password = models.CharField(db_column='password', max_length=10, null=False)


    class Meta:
        managed = False
        db_table = 'users_user'
