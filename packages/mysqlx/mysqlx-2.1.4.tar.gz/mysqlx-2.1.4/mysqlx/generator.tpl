from decimal import Decimal
from datetime import date, datetime
from mysqlx.orm import Model, KeyStrategy


class BaseModel(Model):
    {{__attribute_name__key__}} = '{{__key__}}'
    {{__attribute_name__del_flag__}} = '{{__del_flag__}}'
    {{__attribute_name__update_by__}} = '{{__update_by__}}'
    {{__attribute_name__update_time__}} = '{{__update_time__}}'
    {{__attribute_name__key_strategy__}} = KeyStrategy.DB_AUTO_INCREMENT

    def __init__(self,{% for item in base_columns %}{% if loop.last %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %}{% else %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %},{% endif %}{% endfor %}): {% for item in base_columns %}
        self.{{item.COLUMN_NAME}} = {{item.COLUMN_NAME}} {% endfor %}

{% for meta in metas %}
class {{meta.class_name}}(BaseModel):{% if meta.key != __key__ %}
    {{__attribute_name__key__}} = '{{meta.key}}'{% endif %}
    {{__attribute_name__table__}} = '{{meta.table}}'

    def __init__(self,{% for item in meta.columns %}{% if loop.last %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %}{% else %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %},{% endif %}{% endfor %}):
        super().__init__({% for item in meta.super_columns %}{% if loop.first %}{{item.COLUMN_NAME}}={{item.COLUMN_NAME}}{% else %}, {{item.COLUMN_NAME}}={{item.COLUMN_NAME}}{% endif %}{% endfor %}) {% for item in meta.self_columns %}
        self.{{item.COLUMN_NAME}} = {{item.COLUMN_NAME}} {% endfor %}

{% endfor %}