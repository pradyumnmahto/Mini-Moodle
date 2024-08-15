from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.storage import FileSystemStorage
from .models import User,Course,Assignment,AssignmentSubmission

ROLES = (
    ("Teacher",  "Teacher"),
    ("Student",  "Student"),
)

class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        """Constructor class
        """
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['role'].label = "Role"
        # role = forms.ChoiceField(label="Role", choices= ROLES, widget=forms.RadioSelect, required=True)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['role'].widget.attrs.update(
            {
                'placeholder': 'Choose Role',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'First name is required',
                'max_length': ' First Name is too long'
            },
        }

    def save(self, commit=True):
        """Saves the user model

        Args:
            commit (bool, optional): For committing the model. Defaults to True.

        Returns:
            User: Model is returned
        """
        user = super(UserCreationForm, self).save(commit=False)
        # user.role = self.cleaned_data('role')
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username"
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        """Constructor class
        """
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        """Function to clean the username and passowrd

        Returns:
            User: Cleaned user details
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        """Getter for user

        Returns:
            User: Returns the user model
        """
        return self.user


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'teacher_name', 'course_description']

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].label = "Course Name"
        self.fields['teacher_name'].label = "Teacher Name"
        self.fields['course_description'].label = "Description"

        self.fields['course_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Course Name',
            }
        )
        self.fields['teacher_name'].widget.attrs.update(
            {
                'placeholder': 'Teacher Name',
            }
        )
        self.fields['course_description'].widget.attrs.update(
            {
                'placeholder': 'Description',
            }
        )

    def is_valid(self):
        """Returns if the form is valid or not

        Returns:
            bool: True if valid, False if not valid
        """
        valid = super(CourseCreateForm, self).is_valid()
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        """For saving the model of the course

        Args:
            commit (bool, optional): For committing the model. Defaults to True.

        Returns:
            Course: Returns a course model
        """
        course = super(CourseCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course


class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'marks', 'duration', 'file_types', 'tree']

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Assignment Name"
        self.fields['content'].label = "Content"
        self.fields['marks'].label = "Marks"
        self.fields['duration'].label = "Duration"
        self.fields['file_types'].label = "File Types for submisison"
        self.fields['tree'].label = "Directory Tree"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Enter A Name',
            }
        )
        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Content',
            }
        )
        self.fields['marks'].widget.attrs.update(
            {
                'placeholder': 'Enter Marks',
            }
        )
        self.fields['duration'].widget.attrs.update(
            {
                'placeholder': '3 hour, 2 hour etc ...',
            }
        )
        self.fields['file_types'].widget.attrs.update(
            {
                'placeholder': '.zip, .tar, .tgz, .pdf ....',
            }
        )
        self.fields['tree'].widget.attrs.update(
            {
                'placeholder': 'Upload Directory Tree as txt file',
            }
        )

    def is_valid(self):
        """Checks if the model is valid

        Returns:
            bool: True if valid, False if invalid
        """
        valid = super(AssignmentCreateForm, self).is_valid()
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        """Saves the assignment model to the database

        Args:
            commit (bool, optional): For committing the data. Defaults to True.

        Returns:
            Assignment: The assignment data is returned
        """
        asg = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            asg.save()
        return asg



class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['comment', 'file']

    def __init__(self, *args, **kwargs):
        """Constructor
        """
        super(AssignmentSubmissionForm, self).__init__(*args, **kwargs)
        
        self.fields['comment'].label = "Comment"
        self.fields['file'].label = "Upload File"

        self.fields['comment'].widget.attrs.update(
            {
                'placeholder': 'Enter Comments  Here',
            }
        )
        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )

    def is_valid(self):
        """Checks if the model is valid

        Returns:
            bool: True if valid, False if invalid
        """
        valid = super(AssignmentSubmissionForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        """Saves the assignment model to the database

        Args:
            commit (bool, optional): For committing the data. Defaults to True.

        Returns:
            Assignment: The assignment data is returned
        """
        asg = super(AssignmentSubmissionForm, self).save(commit=False)
        if commit:
            asg.save()
        return asg

class edit_profile_form(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    def is_valid(self):
        valid = super(edit_profile_form, self).is_valid()
        if self.cleaned_data.get('username') or self.cleaned_data.get('email'):
            return True
        return False

class course_register_form(forms.Form):
    course_id = forms.CharField(max_length=6)

class manual_grade_form(forms.Form):
    marks = forms.CharField(max_length=20)
    feedback = forms.CharField(max_length=250)

class manual_grade_all_form(forms.Form):
    csv_file = forms.FileField(required=True)