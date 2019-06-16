from django_tables2 import tables, TemplateColumn
from .models import BasicInfo


class ClienteBasicInfoTable(tables.Table):
    
    Nome = TemplateColumn(template_name = 'customer_table_view_Nome.html')

    class Meta:
        model = BasicInfo
        
        fields = ["tipo_pessoa", "numero_documento_CNPJ", "servico_ativo"]
    
        sequence = ("Nome", "tipo_pessoa", "numero_documento_CNPJ", "servico_ativo")
        
        attrs = {
            'style' :   'font-size: 1em;',
            'tbody' : {
                'id'    :   'js-filter-employee-table'
            }
        }

