from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# from newsportal.newsportal import settings


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


# форма, которая будет выполняться вместо формы по-умолчанию
# то, что она должна выполняться - в settings.py:
# ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        user_email = [user.email]
        # подтверждающее письмо новому пользователю на электронную почту
        html_content = render_to_string(
            'hello_new_user.html',
            {
                'link': settings.SITE_URL,
                'user': user
            }
        )

        msg = EmailMultiAlternatives(
            subject='Вы успешно зарегистрировались на нашем сайте!',
            body='',  # пустой, потому что у нас есть шаблон
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_email
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return user
