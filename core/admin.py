from django.contrib import admin
from core.models import *

from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Tarefa)
class TarefaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'titulo', 'descricao', 'data_expiracao', 'usuario')
    list_filter = ('titulo', 'descricao', 'data_expiracao', 'usuario')

admin.site.unregister(Tarefa)
admin.site.register(Tarefa, TarefaAdmin)
