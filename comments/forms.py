from django_comments.forms import CommentForm
from django_recaptcha.fields import ReCaptchaField


class CustomCommentForm(CommentForm):
    captcha = ReCaptchaField()
