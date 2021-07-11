from django import forms
from .models import Ad
from django.core.files.uploadedfile import InMemoryUploadedFile

# Really simple naturalsize that is missing from django humanize :(
def naturalsize(count):
    fcount = float(count)
    k = 1024
    m = k * k
    g = m * k
    if fcount < k:
        return str(count) + 'B'
    if fcount >= k and fcount < m:
        return str(int(fcount / (k/10.0)) / 10.0) + 'KB'
    if fcount >= m and fcount < g:
        return str(int(fcount / (m/10.0)) / 10.0) + 'MB'
    return str(int(fcount / (g/10.0)) / 10.0) + 'GB'


class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)   

    picture = forms.FileField(required=False, label="File to Upload <<< "+max_upload_limit_text)
    upload_field_name ='picture'

    class Meta:
        model = Ad
        fields = ('title', 'price', 'text', 'picture','tags')
    
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None: return
        if len(pic)> self.max_upload_limit:
            self.add_error('picture', 'FIle Must be <<'+self.max_upload_limit_text+" bytes")
        
    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()
            self.save_m2m()

        return instance
# strip means to remove whitespace from the beginning and the end before storing the column
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
    
# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other