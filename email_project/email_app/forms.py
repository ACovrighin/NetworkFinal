from django import forms

class EmailForm(forms.Form):
    email_sender = forms.EmailField(label='Sender Email', required=True)
    email_receivers = forms.CharField(label='Receiver Emails (Comma Separated)', required=True)
    cc_receivers = forms.CharField(label='CC Receivers (Comma Separated)', required=False)
    subject = forms.CharField(label='Subject', required=True)
    body = forms.CharField(label='Body', widget=forms.Textarea, required=True)
    attachment = forms.FileField(label='Attachment', required=False)
