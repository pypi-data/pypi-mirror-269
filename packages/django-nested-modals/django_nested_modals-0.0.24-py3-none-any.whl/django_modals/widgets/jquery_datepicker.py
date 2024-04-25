from django.forms import DateInput
from ..fields import FieldEx


class DatePicker(DateInput):
    template_name = 'django_modals/widgets/datepicker.html'
    crispy_field_class = FieldEx
    crispy_kwargs = {'appended_text': '<i class="fas fa-calendar-alt fa-fw"></i>', 'input_size': 'input-group-sm'}
