# Desafio

Criar a estrutura de abertura e gestão de ordem de serviço. Existem 2 tipos de usuários no sistema: Cliente e Técnico. O Cliente deve ter as seguintes permissões:

* Abrir uma ordem de serviço
* Visualizar as próprias ordens de serviço abertas

Nesse caso, a partir do menu **Nova Ordem de Serviço**, o cliente será direcionado para um formulário de criação de OS, onde ele colocará o titulo, assunto e demais campos. Ele também terá acesso a uma página onde poderá visualizar todas as ordens de serviço que ele abriu.

O Técnico terá as seguintes permissões:

* Atribuir uma ordem de serviço a si mesmo
* Alterar o status dessa ordem de serviço.

A partir do menu **Ver Ordens de Serviço**, o técnico poderá visualizar todas as ordens de serviço que ainda não foram atribuídas e atribuir a si mesmo. Assim como alterar o status e comentar as ordens de serviço atribuídas a ele.

Para isso devemos trabalhar com a parte de autorização do Django, trabalhando tanto no backend como no frontend.