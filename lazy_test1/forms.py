from django import forms


class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50)  # 텍스트 입력 폼
    # file = forms.FileField()
    image = forms.ImageField()  # 이미지 업로드 할 폼
