from django.shortcuts import  render, redirect,get_object_or_404
from django.contrib.auth import logout, get_user_model
from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.generic import CreateView, FormView,ListView
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from .functions import *
import string, random, csv, os
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from zipfile import ZipFile
import tarfile
import filecmp

User = get_user_model()

def homepage(request):
    """View for the homepage

    Args:
        request (): Request object

    Returns:
        Response object: View for the homepage
    """
    course = Course.objects.all().values()
    return render(request=request, template_name='main/home.html', context = {'course': course})

class RegisterStudentView(CreateView):
    """Class for registering new account"""
    model = User
    form_class = NewUserForm
    template_name = 'main/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('main:login')
        else:
            return render(request, 'main/register.html', {'form': form})


class LoginView(FormView):
    """Class for login view"""
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'main/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")

def password_reset_request(request):
    """View for password reset

    Args:
        request (): Request Object

    Returns:
        View for password reset request
    """
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("main:homepage")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})


def edit_profile(request):
    form = edit_profile_form()
    if not request.user.is_authenticated:
        return reverse_lazy('main:login')
    if request.method=='POST':
        form = edit_profile_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            mail = form.cleaned_data.get('email')
            if not User.objects.filter(username=name) and not User.objects.filter(email=mail):
                if name:
                    request.user.username = name
                if mail:
                    request.user.email = mail
                request.user.save(update_fields=['username','email'])
                messages.success(request, 'Profile Edited successfully !')
                return redirect('main:homepage')
            messages.error(request, 'Username or email already in use')
    form = edit_profile_form()
    return render(request=request, template_name="main/edit_profile.html", context={"form":form})

def view_profile(request):
    return render(request=request, template_name='main/view_profile.html')

def join_course(request, uidb64, token, course_id):
    pk = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=pk)
    user.courses = user.add_course(course_id)
    user.save(update_fields=['courses'])
    return redirect("main:homepage")


class CourseCreateView(CreateView):
    template_name = 'main/course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('main:homepage')

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('main:login')
        if self.request.user.is_authenticated and self.request.user.role != 'Teacher':
            return reverse_lazy('main:login')
        return super().dispatch(self.request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.request.user.courses = self.request.user.add_course(form.instance.course_id)
        self.request.user.save(update_fields=['courses'])
        users = User.objects.all()
        for user in users:
            if user.role == "Teacher":
                continue
            subject = "Register for Course"
            email_template_name = "main/join_course_email.txt"
            c = {
            "email":user.email,
            'domain':'127.0.0.1:8000',
            'site_name': 'Website',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "course_id": form.instance.course_id,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return super(CourseCreateView, self).form_valid(form)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def course_join(request):
    """View for joinging a course

    Args:
        request (): Request Object

    Returns:
        View for joining course is returned
    """
    form = course_register_form()
    if not request.user.is_authenticated:
        return reverse_lazy('main:login')
    if request.user.is_authenticated and request.user.role != 'Student':
        return reverse_lazy('main:login')
    if request.method=='POST':
        form = course_register_form(request.POST)
        if form.is_valid():
            course_id = form.cleaned_data['course_id']
            if Course.objects.filter(course_id=course_id):
                if (not request.user.get_courses()) or (course_id not in request.user.get_courses()):
                    request.user.courses = request.user.add_course(course_id)
                    request.user.save(update_fields=['courses'])
                    messages.success(request, 'Course Registered successfully !')
                    return redirect('main:homepage')
                messages.error(request, 'Course already registered.')
            else:
                messages.error(request, 'An Invlaid Course Code has been entered.')
    form = course_register_form()
    return render(request=request, template_name="main/course_join.html", context={"form":form})


def manual_grade(request, id):
    """View for manual grading

    Args:
        request (): Request Object
        id (): ID of course

    Returns:
        View for manual grading
    """
    form = manual_grade_form()
    if not request.user.is_authenticated:
        return reverse_lazy('main:login')
    if request.user.is_authenticated and request.user.role != 'Teacher':
        return reverse_lazy('main:login')
    if request.method=='POST':
        form = manual_grade_form(request.POST)
        if form.is_valid():
            submisison = get_object_or_404(AssignmentSubmission, id=id)
            submisison.marks = form.cleaned_data['marks']
            submisison.feedback = form.cleaned_data['feedback']
            submisison.save(update_fields=['marks', 'feedback'])
            messages.success(request, 'Grade Updated !')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    form = manual_grade_form()
    return render(request=request, template_name="main/manual_grade.html", context={"form":form})


def manual_grade_all(request, name, title):
    """Manual grading for all registered students

    Args:
        request (): Request Object
        name (string): Name of course
        title (string): Title of assignment

    Returns:
        View of the manual grading portal
    """
    form = manual_grade_all_form()
    if not request.user.is_authenticated:
        return reverse_lazy('main:login')
    if request.user.is_authenticated and request.user.role != 'Teacher':
        return reverse_lazy('main:login')
    if request.method=='POST':
        form = manual_grade_all_form(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            handle_uploaded_file(csv_file)
            submissions = AssignmentSubmission.objects.filter(course_name=name, assignment_title=title)
            with open('media/'+csv_file.name, 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:
                    for foo in submissions:
                        if foo.user.username == row[0]:
                            foo.marks = row[1]
                            foo.feedback = row[2]
                            foo.save(update_fields=['marks','feedback'])
            os.remove('media/'+csv_file.name)
            messages.success(request, 'Grades Updated !')
            prev = request.POST.get('next', '/')
            return HttpResponseRedirect(prev)
    form = manual_grade_all_form()
    return render(request=request, template_name="main/manual_grade_all.html", context={"form":form})


def course_single(request, id):
    course = get_object_or_404(Course, course_id=id)
    assignment=Assignment.objects.all().values()
    if not request.user.is_authenticated:
        return reverse_lazy('main:login')
    return render(request, "main/view_course.html", {'course': course, 'assignment': assignment })


class AssignmentCreateView(CreateView):
    template_name = 'main/create_assignment.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('main:homepage')

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('main:login')
        if self.request.user.is_authenticated and self.request.user.role != 'Teacher':
            return reverse_lazy('main:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        course = Course.objects.get(course_id=self.kwargs['id'])
        form.instance.course_name=course.course_name
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            self.success_url = request.POST.get('next', '/')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            

class AssignmentSubmissionView(CreateView):
    template_name = 'main/submit_assignment.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Assigment'
    }
    success_url = reverse_lazy('main:homepage')

    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('main:login')
        if self.request.user.is_authenticated and self.request.user.role != 'Student':
            return reverse_lazy('main:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        assignment = Assignment.objects.get(id=self.kwargs['id'])
        form.instance.assignment_title = assignment.title
        form.instance.course_name = assignment.course_name
        prev = AssignmentSubmission.objects.filter(user=self.request.user, assignment_title=assignment.title, course_name=assignment.course_name)
        
        
        split_tup=os.path.splitext(form.instance.file.name)
        if split_tup[1]!=assignment.file_types:
            return self.form_invalid(form)
        corr=True
        if assignment.file_types==".zip":
            with ZipFile(form.instance.file, 'r') as zObject:
                zObject.extractall()
            os.system("tree '{0}' > temp.txt".format(split_tup[0]))

            a_file = open("temp.txt", "r")
            lines = a_file.readlines()
            a_file.close()
            lines[0]='.\n'
            new_file = open("temp.txt", "w+")
            for line in lines:
                new_file.write(line)
            new_file. close()
            f='media/'+assignment.tree.name
            corr=filecmp.cmp(f, 'temp.txt')
            os.system("rm temp.txt")
            os.system("rm -r '{0}'".format(split_tup[0]))

       
        if assignment.file_types==".gz":
            handle_uploaded_file(form.instance.file)
            os.system("tar -xvzf media/'{0}'".format(form.instance.file.name))
            os.system("rm -r media/'{0}'".format(form.instance.file.name))
            os.system("tree '{0}' > temp.txt".format(split_tup[0]))
            a_file = open("temp.txt", "r")
            lines = a_file.readlines()
            a_file.close()
            lines[0]='.\n'
            new_file = open("temp.txt", "w+")
            for line in lines:
                new_file.write(line)
            new_file. close()
            f='media/'+assignment.tree.name
            corr=filecmp.cmp(f, 'temp.txt')
            os.system("rm temp.txt")
            os.system("rm -r '{0}'".format(split_tup[0]))

        if not corr:
            return self.form_invalid(form)
        for i in prev:
            i.file.delete()
            i.delete()
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        assignment = Assignment.objects.get(id=self.kwargs['id'])
        form.instance.file_types = assignment.file_types
        if form.is_valid():
            self.success_url = request.POST.get('next', '/')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'main/view_submissions.html'
    context_object_name = 'assignment_submission'
    parent = ''
    @method_decorator(login_required(login_url=reverse_lazy('main:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        f=''
        for x in self.model.objects.all():
            f = x.file.url
            break
        parent = f[:f.rfind('/')]
        os.system('tar -czf ' + parent[1:] + '.tgz ' + parent[1:])
        self.parent = parent + '.tgz'
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = self.parent
        return context

    def get_queryset(self):
        title= self.kwargs['title']
        name = self.kwargs['name']
        return self.model.objects.filter(assignment_title=title , course_name=name).order_by('-id')