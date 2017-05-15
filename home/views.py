from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from .models import *
import mimetypes
import os


def display(request):
    update_attendance()
    update_grades()
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def gallery(request):
    return render(request, "gallery.html")


def payments(request):
    return render(request, "payments.html")


def attendance(request, child_id):
    from .models import Student, Attendance, Parent
    if not request.user.is_authenticated:
        return redirect('/login/')
    if find_teacher(request.user.username) or request.user.is_superuser:
        return render(request, "profile.html", {'error': "you're not allowed to access attendance page."})
    if find_student(request.user.username):  # student
        parent = False
        student = Student.objects.get(pk=find_student(request.user.username))
    else:  # parent
        parent = True
        children = Parent.objects.get(pk=find_parent(request.user.username)).student_set.all()
        if child_id is not None:
            try:
                student = Student.objects.get(pk=child_id)
            except:
                return render(request, "children.html", {'error': 'child not found.'})
            if student not in children:
                return render(request, "children.html", {'error': 'you have no permission to access this child page.'})
        else:
            return redirect("/profile/")
    attendance = Attendance.objects.get(student=student)
    fields = []
    for field in attendance._meta.fields:
        if field.name != 'id' and field.name != 'student' and field.name != 'classroom':
            fields.append(getattr(attendance, field.name))
    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday']
    return render(request, "attendance.html", {'student': student, 'fields': fields, 'parent': parent, 'days': days})


def grades(request, child_id):
    from .models import Student, Grade, Parent
    if not request.user.is_authenticated:
        return redirect('/login/')
    if find_teacher(request.user.username) or request.user.is_superuser:
        return render(request, "profile.html", {'error': "you're not allowed to access grades page."})
    if find_student(request.user.username):  # student
        parent = False
        student = Student.objects.get(pk=find_student(request.user.username))
    else:  # parent
        parent = True
        children = Parent.objects.get(pk=find_parent(request.user.username)).student_set.all()
        if child_id is not None:
            try:
                student = Student.objects.get(pk=child_id)
            except:
                return render(request, "children.html", {'error': 'child not found.'})
            if student not in children:
                return render(request, "children.html", {'error': 'you have no permission to access this child page.'})
        else:
            return redirect("/profile/")
    grades = Grade.objects.get(student=student)
    subjects = get_subjects(None, student.classroom)
    midterm = []
    final = []
    practical = []
    total = []
    for field in grades._meta.fields:
        if field.name != 'id' and field.name != 'student' and field.name != 'classroom':
            if "mid" in field.name:
                try:
                    midterm.append(getattr(grades, field.name))
                except:
                    midterm.append(None)
            elif "final" in field.name:
                try:
                    final.append(getattr(grades, field.name))
                except:
                    final.append(None)
            else:
                try:
                    practical.append(getattr(grades, field.name))
                except:
                    practical.append(None)
    i = 0
    for x in midterm:
        try:
            total.append((midterm[i]+final[i]+practical[i])*100/300)
        except:
            total.append(None)
        i += 1
    return render(request, "grades.html", {'student': student,
                                           'parent': parent,
                                           'subjects': subjects,
                                           'midterm': midterm, 'final': final, 'practical': practical, 'total': total})


def manage_attendance(request, class_id):
    from .models import Teacher
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.user.is_superuser: #admin
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})
    if request.user.is_staff: # teacher
        teacher = Teacher.objects.get(pk=find_teacher(request.user.username))
        classrooms = get_classrooms(teacher)
        if class_id is None:
            return render(request, "manage attendance.html", {'classrooms': classrooms})
        else:
            try:
                students = classrooms[int(class_id)-1].student_set.all()
                student_ids = []
                for x in students:
                    student_ids.append(x.pk)
            except:
                return render(request, "manage attendance.html", {'error': "You're not allowed to access this page."})
            return render(request, "manage attendance.html", {'students': students,
                                                              'student_ids': student_ids,
                                                              'class_id': class_id})
    else: # student or parent
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})


def save_attendance(request):
    from .models import Teacher, Attendance
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.user.is_superuser: #admin
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})
    if not request.user.is_staff:
        return redirect('/profile/')
    else:
        if request.method == "POST":
            teacher = Teacher.objects.get(pk=find_teacher(request.user.username))
            classrooms = get_classrooms(teacher)
            students = classrooms[int(request.POST['class_id']) - 1].student_set.all()
            for student in students:
                attendance = Attendance.objects.get(student=student)
                for field in attendance._meta.fields:
                    if field.name != 'id' and field.name != 'student' and field.name != 'classroom':
                        try:
                            if request.POST['%s_%s' % (student.pk, field.name)] == 'on':
                                setattr(attendance, field.name, True)
                        except:
                            setattr(attendance, field.name, False)
                attendance.save()
    return render(request, "manage attendance.html", {'error': "Attendance saved successfully."})


def manage_grades(request, class_id):
    from .models import Teacher
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.user.is_superuser: #admin
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})
    if request.user.is_staff: # teacher
        teacher = Teacher.objects.get(pk=find_teacher(request.user.username))
        classrooms = get_classrooms(teacher)
        if class_id is None:
            return render(request, "manage grades.html", {'classrooms': classrooms})
        else:
            try:
                classroom = classrooms[int(class_id)-1]
            except:
                return render(request, "manage grades.html", {'error': "You're not allowed to access this page."})
            subjects = get_subjects(teacher, classroom)
            try:
                students = classroom.student_set.all()
                student_ids = []
                for x in students:
                    student_ids.append(x.pk)
            except:
                return render(request, "manage grades.html", {'error': "You're not allowed to access this page."})
            return render(request, "manage grades.html", {'students': students,
                                                          'student_ids': student_ids,
                                                          'class_id': class_id,
                                                          'subjects': subjects})
    else: # student or parent
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})


def save_grades(request):
    from .models import Teacher, Grade
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.user.is_superuser: #admin
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})
    if not request.user.is_staff:
        return redirect('/profile/')
    else:
        if request.method == "POST":
            teacher = Teacher.objects.get(pk=find_teacher(request.user.username))
            classrooms = get_classrooms(teacher)
            students = classrooms[int(request.POST['class_id']) - 1].student_set.all()
            for student in students:
                grades = Grade.objects.get(student=student)
                for field in grades._meta.fields:
                    if field.name != 'id' and field.name != 'student' and field.name != 'classroom':
                        if 'mid' in field.name:
                            try:
                                setattr(grades, field.name, int(request.POST['%s_%smid' % (student.pk,
                                                                                           field.verbose_name.replace(' Midterm',""))]))
                            except:
                                setattr(grades, field.name, None)
                        elif 'final' in field.name:
                            try:
                                setattr(grades, field.name, int(request.POST['%s_%sfinal' % (student.pk,
                                                                                             field.verbose_name.replace(' Final',""))]))
                            except:
                                setattr(grades, field.name, None)
                        else:
                            try:
                                setattr(grades, field.name, int(request.POST['%s_%spractical' % (student.pk,
                                                                                                 field.verbose_name.replace(' Practical',""))]))
                            except:
                                setattr(grades, field.name, None)
                grades.save()
    return render(request, "manage grades.html", {'error': "Grades saved successfully."})


def view_assignments(request, class_id, student_id):
    from .models import Student, Teacher, Classroom, Solved_Assignment
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.user.is_superuser: #admin
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})
    if request.user.is_staff:
        teacher = Teacher.objects.get(pk=find_teacher(request.user.username))
        classrooms = get_classrooms(teacher)
        classroom_ids = []
        for x in classrooms:
            classroom_ids.append(x.pk)
        if class_id is None: # 'view_assignments/'
            return render(request, "view assignments.html", {'classrooms': classrooms, 'classroom_ids': classroom_ids})
        elif student_id is not None: # 'view_assignments/2/3'
            try:
                classroom = Classroom.objects.get(pk=class_id)
                student = Student.objects.get(pk=student_id)
            except:
                return render(request, "view assignments.html", {'error': 'Student not found.'})
            if student.classroom != classroom:
                return render(request, "view assignments.html", {'error': 'Student not found in this class.'})
            else:
                subjects = get_subjects(teacher, Classroom.objects.get(pk=class_id))
                try:
                    assignment_list_old = Solved_Assignment.objects.filter(student=student)
                    assignment_list = []
                    for assignment in assignment_list_old:
                        if assignment.assignment.subject in subjects:
                            assignment_list.append(assignment)
                    return render(request, "view assignments.html", {'assignment_list': assignment_list})
                except:
                    return render(request, "view assignments.html", {'error': 'Assignments not found.'})
        else: # 'view_assignments/2/'
            try:
                classroom = Classroom.objects.get(pk=class_id)
                if classroom not in classrooms:
                    return render(request, "view assignments.html", {'error': "You're not allowed to access this page."})
                else:
                    students = classroom.student_set.all()
                    student_ids = []
                    for x in students:
                        student_ids.append(x.pk)
            except:
                return render(request, "view assignments.html", {'error': "You're not allowed to access this page."})
            return render(request, "view assignments.html", {'students': students,
                                                             'student_ids': student_ids,
                                                             'class_id': class_id})
    else:
        return render(request, "profile.html", {'error': "you're not allowed to access this page."})


# get classrooms that belongs to this teacher
def get_classrooms(teacher):
    from .models import Classroom
    classrooms = []
    for x in Classroom.objects.all():
        for field in x._meta.fields:
            if teacher == getattr(x, field.name):
                classrooms.append(x)
                break
    return classrooms


# get subjects that belongs to this teacher
def get_subjects(teacher, classroom):
    subjects = []
    for field in classroom._meta.fields:
        if teacher:
            if teacher == getattr(classroom, field.name):
                subjects.append(field.verbose_name)
        elif field.name != 'id' and field.name != 'year' and field.name != 'num':
            subjects.append(field.verbose_name)
    return subjects


def lectures(request, lec_id):
    from .models import Student, Lecture
    if not request.user.is_authenticated:
        return redirect('/login/')
    if find_student(request.user.username):  # student
        student = Student.objects.get(pk=find_student(request.user.username))
        subjects = get_subjects(None, student.classroom)
        if lec_id is not None:
            try:
                lecture_list = Lecture.objects.filter(classroom=student.classroom, subject=subjects[int(lec_id)-1])
            except:
                return render(request, "lectures.html", {'lec_error': 'Lectures not found.', 'student': student})
            query = request.GET.get("q")
            if query:
                lecture_list = lecture_list.filter(title__icontains=query)
            return render(request, "lectures.html", {'lecture_list': lecture_list, 'student': student, 'lec_id': lec_id})
        else:
            return render(request, "lectures.html", {'subjects': subjects, 'student': student})
    else:  # parent
        return render(request, "profile.html", {'error': "you're not allowed to access lectures page.", 'parent': True})


def assignments(request, subject_id):
    from .models import Student, Assignment
    if not request.user.is_authenticated:
        return redirect('/login/')
    if find_student(request.user.username):  # student
        student = Student.objects.get(pk=find_student(request.user.username))
        subjects = get_subjects(None, student.classroom)
        if subject_id is not None:
            try:
                assignment_list_old = Assignment.objects.filter(classroom=student.classroom, subject=subjects[int(subject_id)-1])
            except:
                return render(request, "assignments.html", {'task_error': 'Assignment not found.', 'student': student})
            query = request.GET.get("q")
            if query:
                assignment_list_old = assignment_list_old.filter(title__icontains=query)
            assignment_list = []
            for assignment in assignment_list_old:
                if verify_assignment(student, assignment): # not found
                    assignment_list.append(assignment)
            assignment_ids = []
            for x in assignment_list:
                assignment_ids.append(x.pk)
            return render(request, "assignments.html", {'assignment_list': assignment_list, 'assignment_ids': assignment_ids,
                                                        'student': student, 'subject_id': subject_id})
        else:
            return render(request, "assignments.html", {'subjects': subjects, 'student': student})
    else:  # parent
        return render(request, "profile.html", {'error': "you're not allowed to access assignments page.", 'parent': True})


def assignments_solve(request, task_id):
    from .models import Assignment, Student
    if not request.user.is_authenticated:
        return redirect('/login/')
    if not find_student(request.user.username):
        return redirect('/profile/')
    elif task_id is not None:
        student = Student.objects.get(pk=find_student(request.user.username))
        try:
            assignment = Assignment.objects.get(pk=task_id)
        except:
            return render(request, "assignments.html", {'task_error': 'Assignment not found.', 'student': student})
        assignment_list = Assignment.objects.filter(classroom=student.classroom)
        if assignment in assignment_list:
            if verify_assignment(student, assignment):
                return render(request, "assignments_solve.html", {'assignment': assignment, 'student': student})
        return render(request, "assignments.html", {'task_error': 'Assignment not found.', 'student': student})
    else:
        return redirect('/assignments/')


def save_assignment(request):
    from .models import Student, Assignment, Solved_Assignment
    if not request.user.is_authenticated:
        return redirect('/login/')
    if not find_student(request.user.username):
        return redirect('/profile/')
    else:
        if request.method == "POST":
            student = Student.objects.get(pk=request.POST['student_pk'])
            assignment = Assignment.objects.get(pk=request.POST['task_id'])

            solved_assignment = Solved_Assignment.objects.create(link=request.POST['solution'],
                                                                 student=student,
                                                                 assignment=assignment)
            solved_assignment.save()
    return render(request, "manage attendance.html", {'error': "Assignment uploaded successfully."})


# to verify that this student haven't solved this assignment yet
def verify_assignment(student, assignment):
    from .models import Solved_Assignment
    try:
        Solved_Assignment.objects.get(student=student, assignment=assignment)
        return False # found
    except:
        return True # not found


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/profile/')
    return render(request, "login.html")


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    elif request.user.is_superuser:  # admin
        return redirect('/admin/')
    else:
        return type_redirect(request)


def child(request, child_id):
    from .models import Student, Parent
    if not request.user.is_authenticated:
        return redirect('/login/')
    try:
        children = Parent.objects.get(pk=find_parent(request.user.username)).student_set.all()
    except:
        return render(request, "children.html", {'error': 'you have no permission to access this child page.'})
    if child_id is not None:
        try:
            kid = Student.objects.get(pk=child_id)
        except:
            return render(request, "children.html", {'error': 'child not found.'})
        if kid not in children:
            return render(request, "children.html", {'error': 'you have no permission to access this child page.'})
        else:
            return render(request, "profile.html", {'student': Student.objects.get(pk=child_id), 'parent': True})
    else:
        return render(request, "children.html", {'children': children})


def login_now(request):
    if request.user.is_authenticated:
        return redirect('/profile/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                update_attendance()
                update_grades()
                return type_redirect(request)
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid ID or password, please try again.'})
    return render(request, 'login.html')


def logout_now(request):
    logout(request)
    form = User(request.POST or None)
    return render(request, 'login.html', {"form": form})


# to search through the db to find exact username
def find_student(username):
    from .models import Student
    for x in Student.objects.all():
        if username == Student.objects.get(pk=x.pk).username.__str__():
            return x.pk
    return False


def find_parent(username):
    from .models import Parent
    for x in Parent.objects.all():
        if username == Parent.objects.get(pk=x.pk).username.__str__():
            return x.pk
    return False


def find_teacher(username):
    from .models import Teacher
    for x in Teacher.objects.all():
        if username == Teacher.objects.get(pk=x.pk).username.__str__():
            return x.pk
    return False


def download(request, file_name, path):
    path = path + file_name
    if request.user.is_authenticated:
        if os.path.exists(path):
            response = HttpResponse(
                FileResponse(open(path, 'rb')),
                content_type=mimetypes.guess_type(path)[0])
            response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
            return response
        else:
            return HttpResponse("File not found.")
    return HttpResponse("You don't have permission to download this file.")


def update_attendance():
    from .models import Student, Attendance
    for x in Student.objects.all():
        try:
            Attendance.objects.get(pk=x.pk)
        except:
            Attendance.objects.create(student=Student.objects.get(pk=x.pk),
                                      classroom=Student.objects.get(pk=x.pk).classroom)

def update_grades():
    from .models import Student, Grade
    for x in Student.objects.all():
        try:
            Grade.objects.get(pk=x.pk)
        except:
            Grade.objects.create(student=Student.objects.get(pk=x.pk),
                                      classroom=Student.objects.get(pk=x.pk).classroom)


def type_redirect(request):
    from .models import Student, Teacher
    if request.user.is_superuser: # admin
        return redirect('/admin/')
    elif request.user.is_staff: #teacher
        return render(request, "profile.html",
                      {'teacher': Teacher.objects.get(pk=find_teacher(request.user.username)), 'parent': False})
    else:
        if find_student(request.user.username):  # student
            return render(request, "profile.html",
                          {'student': Student.objects.get(pk=find_student(request.user.username)), 'parent': False})
        else:  # parent
            return redirect('/child/')


def validate_nonzero(value):
    if value == 0:
        raise ValidationError('Zero is not allowed.')
