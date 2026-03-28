
from typing import List

# A biblioteca typing é utilizada para tipagem dos dados em Python. No caso da função abaixo, estamos indicando que ela irá retornar uma lista contendo ou não strings.
def campos_nao_preenchidos(nome: str, sobrenome: str, endereco: str) -> List[str|None]:
    campos = []

    if nome.strip() == "":
        campos.append("nome")

    if sobrenome.strip() == "":
        campos.append("sobrenome")

    if endereco.strip() == "":
        campos.append("endereco")

    return campos