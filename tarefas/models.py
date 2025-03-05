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

class Semana(Document):
    usuario = IntField(required=True)
    indicador = StringField(required=True)
    segunda = DateField(null=True)
    terca = DateField(null=True)
    quarta = DateField(null=True)
    quinta = DateField(null=True)
    sexta = DateField(null=True)
    sabado = DateField(null=True)
    domingo = DateField(null=True)