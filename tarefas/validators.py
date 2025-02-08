FREQUENCIA = [
    ('Domingo', 0),
    ('Segundo-Feira', 1),
    ('Terça-Feira', 2),
    ('Quarta-Feira', 3),
    ('Quinta-Feira', 4),
    ('Sexta=Feira', 5),
    ('Sabado', 6),
    ('Todos os dias', 7),
]

def repeticoes_invalida(repeticoes):
    repeticao_invalida = False

    if repeticoes:
        valores_validos = [valor for _, valor in FREQUENCIA]
        for repeticao in repeticoes:
            if repeticao not in valores_validos:
                repeticao_invalida = True

    return repeticao_invalida