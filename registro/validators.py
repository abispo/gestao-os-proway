from django.contrib.auth.models import User

"""
Se quisermos, além de indicar o tipo do parâmetro que está sendo recebido, podemos também indicar o tipo de retorno da função, utilizando a sintaxe de seta (->). No caso abaixo, estamos indicando que a função todos_dados_foram_preenchidos vai retornar um valor booleano.
"""
def todos_dados_foram_preenchidos(*args: tuple) -> bool:
    return all(args)

def nome_de_usuario_ja_existe(nome_de_usuario: str) -> User | None:
    return User.objects.filter(username=nome_de_usuario).first()

def senhas_nao_sao_iguais(senha: str, confirmar_senha: str) -> bool:
    return senha.strip() != confirmar_senha.strip()