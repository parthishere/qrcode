from django import forms
from accounts.models import Invitee
from django.core.exceptions import ValidationError
from events.models import Event


class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("event_name", "event_date", "about", "contact_number","contact_number_2","contact_email","contact_email_2", "fast_check", "pre_define_pass", "predefined_pass_image")
        
        widgets = {
                'event_date' : DateTimePickerInput(),
            }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
class InviteeForm(forms.ModelForm):
    class Meta:
        model = Invitee
        fields = ("name", "email", "phone_number", "other_info", "recognized")
    def __init__(self, *args, **kwargs):
        super(InviteeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
class FileForm(forms.Form):
    excel_file = forms.FileField(required=True,
        label = 'Select a file',
        help_text = 'maximum file size: 50mb',
        allow_empty_file=False)
    
    def clean(self):
        cleaned_data = super(FileForm, self).clean()
        file = self.cleaned_data['excel_file']
        if file:
            filename = file.name
            if filename.endswith('.xlsx') or filename.endswith('.xlx'):
                pass
            else:
                print('File is NOT a excel')
                raise forms.ValidationError("File is not a xlsx or xlx. Please upload only xlsx or xlx files")

        return file
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
        