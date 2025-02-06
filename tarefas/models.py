from mongoengine import Document, StringField, DateField, BooleanField, ListField, IntField

class Tarefas(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    agendamento = DateField(blank=True)

class Repeticoes(Document):
    usuario = IntField(required=True)
    descricao = StringField(required=True)
    frequente = BooleanField(default=False)
    repeticoes = ListField(StringField(), blank=True)

