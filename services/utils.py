from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View


class SuperUserRequiredMixin(UserPassesTestMixin, View):
    """
    Restricts view to superusers. Code is from
    https://stackoverflow.com/questions/12003736/django-login-required-decorator-for-a-superuser
    """
    def test_func(self):
        return self.request.user.is_superuser
