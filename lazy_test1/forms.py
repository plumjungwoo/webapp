from django import forms
from .models import ImageUploadModel


class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50)  # 텍스트 입력 폼
    # file = forms.FileField()
    image = forms.ImageField()  # 이미지 업로드 할 폼


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('description', 'document')
