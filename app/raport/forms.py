from django import forms

class TaskCSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Plik CSV",
        help_text="CSV z kolumnami Column1 (title) i Column2 (jira_id).",
    )