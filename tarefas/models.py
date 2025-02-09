from mongoengine import Document, StringField, DateField, ListField, IntField

class Tarefas(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    agendamento = DateField(blank=True, default=None)

class Repeticoes(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    repeticoes = ListField(IntField())