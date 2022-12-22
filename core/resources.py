from import_export import resources
from core.models import Tarefa


class TarefaResource(resources.ModelResource):
    class Meta:
        model = Tarefa
    