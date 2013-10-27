from django import forms

# The choices property of ChoiceField evaluates the choices field with a list(),
# such that the iterator is only evaluated once. We don't want that, so we
# override the property here.


class NoCacheChoiceField(forms.ChoiceField):

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        self._choices = self.widget.choices = value

    choices = property(_get_choices, _set_choices)
