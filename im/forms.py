from django import forms


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Upload Excel File")

class ExcelUploadSaleForm(forms.Form):
    file = forms.FileField()

class ExcelUploadInventoryForm(forms.Form):
    file = forms.FileField()

class ExcelUploadWorkingDaysForm(forms.Form):
    file = forms.FileField()
