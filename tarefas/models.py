from mongoengine import Document, StringField, DateField, ListField, IntField, ReferenceField
from datetime import date

class Tarefas(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    agendamento = DateField(default=date(9999, 12, 31))
    comentarios = StringField(blank=True, default=None)

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
    segunda = ReferenceField(Dia)
    terca = ReferenceField(Dia)
    quarta = ReferenceField(Dia)
    quinta = ReferenceField(Dia)
    sexta = ReferenceField(Dia)
    sabado = ReferenceField(Dia)
    domingo = ReferenceField(Dia)