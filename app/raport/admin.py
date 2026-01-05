import csv
import io

from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path

from .forms import TaskCSVImportForm
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("jira_id", "title")
    search_fields = ("jira_id", "title")

    change_list_template = "admin/yourapp/task/change_list.html"  # <- ZMIEŃ yourapp na app_label

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.import_csv_view),
                name="task_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv_view(self, request):
        if request.method == "POST":
            form = TaskCSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                f = form.cleaned_data["csv_file"]
                raw = f.read().decode("utf-8-sig", errors="replace")

                # wykryj delimiter (Excel PL często daje ';')
                try:
                    dialect = csv.Sniffer().sniff(raw[:4096], delimiters=";,\t")
                except csv.Error:
                    dialect = csv.excel
                    dialect.delimiter = ";"

                reader = csv.DictReader(io.StringIO(raw), dialect=dialect)
                fieldnames = reader.fieldnames or []

                # preferuj Column1/Column2, ale fallback na pierwsze 2 kolumny
                col_title = "Column1" if "Column1" in fieldnames else (fieldnames[0] if len(fieldnames) > 0 else None)
                col_jira  = "Column2" if "Column2" in fieldnames else (fieldnames[1] if len(fieldnames) > 1 else None)

                if not col_title or not col_jira:
                    messages.error(
                        request,
                        f"Nie znaleziono kolumn. Wymagane: Column1 (title) i Column2 (jira_id). "
                        f"Znalezione nagłówki: {fieldnames}"
                    )
                    return redirect("..")

                rows = []
                for row in reader:
                    title = (row.get(col_title) or "").strip()
                    jira_id = (row.get(col_jira) or "").strip()
                    if jira_id:
                        rows.append((jira_id, title))

                if not rows:
                    messages.warning(request, "Plik nie zawiera żadnych rekordów z jira_id.")
                    return redirect("..")

                jira_ids = [j for (j, _) in rows]
                existing = set(
                    Task.objects.filter(jira_id__in=jira_ids).values_list("jira_id", flat=True)
                )

                to_create = [
                    Task(jira_id=jira_id, title=title)
                    for (jira_id, title) in rows
                    if jira_id not in existing
                ]

                Task.objects.bulk_create(to_create, ignore_conflicts=True)

                messages.success(
                    request,
                    f"Import zakończony. Nowe: {len(to_create)} | Pominięte (już istnieją): {len(existing)}"
                )
                return redirect("..")
        else:
            form = TaskCSVImportForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Import Tasków z CSV",
            "form": form,
        }
        return render(request, "admin/task_import_csv.html", context)