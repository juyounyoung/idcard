import datetime

from django.db import models


# Create your models here.
class student(models.Model):
    school_ID = models.CharField(db_column='school_ID', max_length=20, null=False, unique=True)
    student_ID = models.CharField(db_column='student_ID', max_length=20, null=False, unique=True)
    board_ID = models.CharField(db_column='board_ID', max_length=20, null=False, unique=True)
    student_group = models.CharField(db_column='student_group', max_length=20, null=True)
    student_name = models.CharField(db_column='student_name', max_length=20)
    student_rn = models.CharField(db_column='student_rn', max_length=14)
    city = models.CharField(db_column='city', max_length=15)
    street_number = models.CharField(db_column='street_number', max_length=15)
    detail_address = models.CharField(db_column='detail_address', max_length=30)
    student_phone = models.CharField(db_column='student_phone', max_length=15)
    student_img = models.CharField(db_column='student_img', max_length=255)

    def __str__(self):
        return self.school_ID

    class Meta:
        managed = False
        db_table = 'student'


class school_info(models.Model):
    school_ID = models.CharField(db_column='school_ID', max_length=20, primary_key=True)
    school_name = models.CharField(db_column='school_name', max_length=25)
    school_address = models.CharField(db_column='school_address', max_length=100)
    school_tel = models.CharField(db_column='school_tel', max_length=100)

    class Meta:
        managed = False
        db_table = 'school_info'

class Users_user(models.Model):
    school_ID = models.CharField(db_column='school_ID', max_length=20, primary_key=True)
    password = models.CharField(db_column='password', max_length=128, null=False)
    last_login = models.DateTimeField(db_column='last_login', auto_now=True)
    login_trial = models.IntegerField(db_column='login_trial', default=0)


    class Meta:
        managed = False
        db_table = 'users'

class Board(models.Model):
    school_ID = models.ForeignKey(student, db_column='school_ID', on_delete=models.CASCADE, null=False)
    title = models.CharField(db_column='title', max_length=100, null=False)
    school_name = models.CharField(db_column='school_name', max_length=10, null=False)
    # reporting_date = models.DateTimeField(db_column='reporting_date', auto_now_add=True)
    created_date = models.DateTimeField(db_column='created_date', auto_now_add=True)
    modified_date = models.DateTimeField(db_column='modified_date', auto_now=True)
    hit_count = models.PositiveIntegerField(db_column='hit_count', default=0)
    filename = models.CharField(db_column='filename', max_length=64, null=True)
    del_yn = models.IntegerField(db_column='del_yn', default=0)
    final_yn = models.IntegerField(db_column='final_yn', default=0)

    class Meta:
        managed = False
        db_table = 'board_list'