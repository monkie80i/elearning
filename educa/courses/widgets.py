from django.forms import FileInput

class MyFileInput(FileInput):
    template_name = 'widgets/my_file_input.html'
    initial_text = 'Currently'
    input_text = 'Change'
    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, 'url', False))

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        if self.is_initial(value):
            return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'is_initial': self.is_initial(value),
            'initial_text': self.initial_text,
            'input_text': self.input_text,
        })
        return context