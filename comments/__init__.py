def get_model():
    from .models import CustomComment
    return CustomComment


def get_form():
    from .forms import CustomCommentForm
    return CustomCommentForm
