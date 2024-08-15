from django.db.models import FileField
from django.forms import forms
from django.utils.translation import gettext_lazy as _
import mimetypes

class ContentTypeRestrictedFileField(FileField):

    def __init__(self, *args, **kwargs):
        """Constructor function
        """
        self.content_types = kwargs.pop("content_types")
        self.types = []
        mimetypes.init()
        for i in self.content_types:
            i.strip()
            self.types.append(mimetypes.types_map[i])

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """Function to clean data which is given

        Returns:
            Cleaned version of data
        """
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type not in self.types:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass

        return data