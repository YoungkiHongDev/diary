from django import forms
from diary.models import Write


class WriteForm(forms.ModelForm):
    class Meta:
        model = Write
        fields = ['board_subject', 'board_content', 'board_emo', 'board_img', 'board_tag']
        