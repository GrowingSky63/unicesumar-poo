Notas:

O projeto está bem comentado, mas seguem algumas notas que não eram pertinentes permanecerem no código:
# models.py:
    No python, não existe restrição para variáveis e métodos privados, a convenção é: se começa com _, é privado e não devo mexer, mas se eu quiser, eu posso.

    Em python, uma estrutura mais viável para representar uma classe seria muito mais enxuta, algo como:
    ```
    from dataclasses import dataclass

    @dataclass
    class Produto:
        id: int
        nome: str
        preco: float
        quantidade: int
    ```

    Caso seja necessário implementar mais regras de validação ou regras de negócio da entidade, talvez seja necessário utilizar outras bibliotecas e criar métodos de validação, mas para aplicações simples, o modelo não passará de 10 linhas, devido a desnecessidade de criar getters e setters.

Para testar o código, recomendamos:

1. clonar o repositório
 - git clone https://github.com/GrowingSky63/unicesumar-poo eric-e-tata-poo
 - cd eric-e-tata-poo

2. Verificar versão do python
 - python -V ou python --version
 O código foi feito na versão 3.15.5, mas é pra rodar em qualquer versão acima de 3.13

3. Executar o código
 - python -m product_registrar.MVC.main