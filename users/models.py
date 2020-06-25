from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return f'name: {self.name}, nickname: {self.nickname}, password: {self.password}, birthday: {self.birthday}, email: {self.email}, phone: {self.phone}'

    class Meta:
        db_table = 'users'