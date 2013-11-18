from django import forms
from postman.forms import WriteForm


class WriteFormHideRecipients(WriteForm):

    def __init__(self, *args, **kwargs):
        super(WriteFormHideRecipients, self).__init__(*args, **kwargs)
        self.fields['recipients'].widget = forms.HiddenInput()
        self.fields['body'].required = True

    class Meta(WriteForm.Meta):
        pass
