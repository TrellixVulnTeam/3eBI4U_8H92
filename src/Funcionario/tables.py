from django_tables2 import tables, TemplateColumn
from .models import BasicInfo


class FuncionarioBasicInfoTable(tables.Table):
    
    Nome = TemplateColumn(template_name = 'employee_table_view_employee.html')

    class Meta:
        model = BasicInfo
        
        fields = ["ultimo_nome", "data_nascimento", "genero", "numero_documento_CPF", "status"]
    
        sequence = ("Nome", "ultimo_nome", "data_nascimento", "genero", "numero_documento_CPF", "status")
        
        attrs = {
            'style' : 'font-size: 1em;'
        }
