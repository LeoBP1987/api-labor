from mongoengine import Document, StringField, DateField, ListField, IntField, ReferenceField, NULLIFY
from datetime import date

class Tarefas(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    agendamento = DateField(default=date(9999, 12, 31))
    comentarios = StringField(null=True, default=None)

class Repeticoes(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    repeticoes = ListField(IntField())

class Dia(Document):
    usuario = IntField(required=True)
    dia = DateField(required=True)
    tarefas = ListField(ReferenceField(Tarefas))

class Semana(Document):
    usuario = IntField(required=True)
    indicador = StringField(required=True)
    segunda = ReferenceField(Dia, reverse_delete_rule=NULLIFY)
    terca = ReferenceField(Dia, reverse_delete_rule=NULLIFY)
    quarta = ReferenceField(Dia, reverse_delete_rule=NULLIFY)
    quinta = ReferenceField(Dia, reverse_delete_rule=NULLIFY)
    sexta = ReferenceField(Dia, reverse_delete_rule=NULLIFY)
    sabado = ReferenceField(Dia, reverse_delete_rule=NULLIFY)
    domingo = ReferenceField(Dia, reverse_delete_rule=NULLIFY)