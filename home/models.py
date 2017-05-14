from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from . import views


class Teacher(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50,
                               choices=(('Arabic', 'Arabic'),
                                        ('Maths', 'Maths'),
                                        ('English', 'English'),
                                        ('Physics', 'Physics'),
                                        ('Chemistry', 'Chemistry')),
                               default=None, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female')), default=1)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    year = models.PositiveIntegerField(validators=[MaxValueValidator(6), views.validate_nonzero], default=None)
    num = models.PositiveIntegerField(validators=[MaxValueValidator(15), views.validate_nonzero], default=None)
    subject1teacher = models.ForeignKey(Teacher, related_name='+', default=None, verbose_name='Arabic')
    subject2teacher = models.ForeignKey(Teacher, related_name='+', default=None, verbose_name='Maths')
    subject3teacher = models.ForeignKey(Teacher, related_name='+', default=None, verbose_name='English')
    subject4teacher = models.ForeignKey(Teacher, related_name='+', default=None, verbose_name='Physics')
    subject5teacher = models.ForeignKey(Teacher, related_name='+', default=None, verbose_name='Chemistry')

    def __str__(self):
        return self.year.__str__() + ' - ' + self.num.__str__()


class Parent(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female')), default=1)
    phone = models.PositiveIntegerField()
    mail = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female')), default=1)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(15), views.validate_nonzero], default=None)
    address = models.CharField(max_length=250)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(6), views.validate_nonzero], default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    title = models.CharField(max_length=50)
    subject = models.CharField(max_length=50,
                               choices=(('Arabic', 'Arabic'),
                                        ('Maths', 'Maths'),
                                        ('English', 'English'),
                                        ('Physics', 'Physics'),
                                        ('Chemistry', 'Chemistry')),
                               default=None, null=True, blank=True)
    description = models.CharField(max_length=1000, default=None)
    file = models.FileField(upload_to='./lectures/', default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    subject = models.CharField(max_length=50,
                               choices=(('Arabic', 'Arabic'),
                                        ('Maths', 'Maths'),
                                        ('English', 'English'),
                                        ('Physics', 'Physics'),
                                        ('Chemistry', 'Chemistry')),
                               default=None, null=True, blank=True)
    file = models.FileField(upload_to='./assignments/', default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Solved_Assignment(models.Model):
    link = models.CharField(max_length=1000)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.__str__() + ' - ' + self.assignment.__str__()


class Attendance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)
    day1 = models.NullBooleanField(verbose_name='Sunday')
    day2 = models.NullBooleanField(verbose_name='Monday')
    day3 = models.NullBooleanField(verbose_name='Tuesday')
    day4 = models.NullBooleanField(verbose_name='Wednesday')
    day5 = models.NullBooleanField(verbose_name='Thursday')

    def __str__(self):
        return self.student.name


class Grade(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)
    subject1mid = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Arabic Midterm', null=True, blank=True, default=None)
    subject1final = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Arabic Final', null=True, blank=True, default=None)
    subject1practical = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Arabic Practical', null=True, blank=True, default=None)
    subject2mid = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Maths Midterm', null=True, blank=True, default=None)
    subject2final = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Maths Final', null=True, blank=True, default=None)
    subject2practical = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Maths Practical', null=True, blank=True, default=None)
    subject3mid = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='English Midterm', null=True, blank=True, default=None)
    subject3final = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='English Final', null=True, blank=True, default=None)
    subject3practical = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='English Practical', null=True, blank=True, default=None)
    subject4mid = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Physics Midterm', null=True, blank=True, default=None)
    subject4final = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Physics Final', null=True, blank=True, default=None)
    subject4practical = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Physics Practical', null=True, blank=True, default=None)
    subject5mid = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Chemistry Midterm', null=True, blank=True, default=None)
    subject5final = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Chemistry Final', null=True, blank=True, default=None)
    subject5practical = models.PositiveIntegerField(validators=[MaxValueValidator(100), views.validate_nonzero], verbose_name='Chemistry Practical', null=True, blank=True, default=None)

    def __str__(self):
        return self.student.name
