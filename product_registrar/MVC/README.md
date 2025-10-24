<!-- ================================================================== -->
# Cadastro de Produtos (MVC) e Módulo de Projetos & Tarefas
<!-- ================================================================== -->

## Notas Iniciais
O projeto está bem comentado, mas seguem algumas notas que não eram pertinentes permanecerem no código:

### models.py:
No python, não existe restrição para variáveis e métodos privados, a convenção é: se começa com _, é privado e não devo mexer, mas se eu quiser, eu posso.

Em python, uma estrutura mais viável para representar uma classe seria muito mais enxuta, algo como:

```python
from dataclasses import dataclass

@dataclass
class Produto:
  id: int
  nome: str
  preco: float
  quantidade: int
```

Caso seja necessário implementar mais regras de validação ou regras de negócio da entidade, talvez seja necessário utilizar outras bibliotecas e criar métodos de validação, mas para aplicações simples, o modelo não passará de 10 linhas, devido a desnecessidade de criar getters e setters.

---

## Como Testar o Código
Para testar o código, recomendamos:

### 1. Clonar o repositório
```bash
git clone https://github.com/GrowingSky63/unicesumar-poo eric-e-tata-poo
cd eric-e-tata-poo
```

### 2. Verificar versão do python
```bash
python -V
```
Ou
```bash
python --version
```
O código foi feito na versão 3.15.5, mas é pra rodar em qualquer versão acima de 3.13

### 3. Executar o código
```bash
python -m product_registrar.MVC.main
```

---

## Módulo de Projetos e Tarefas (Aula 03)

Foi adicionado um módulo complementar seguindo o padrão MVC para gerenciar Projetos e suas Tarefas.

Tentamos manter a mesma estruturação com getters e setters. Porêm, a classe de status se encaixa melhor em python, herdando de Enum.

### Novos Models
- `Projeto(id, nome, tarefas)`
- `Tarefa(descricao, responsavel, status)` onde `status` pode ser: `pendente`, `em_andamento`, `concluida`.

### Novos Controllers
- `ProjetoController`: adiciona e lista projetos.
- `TarefaController`: adiciona, lista e filtra tarefas por status dentro de um projeto.

### Novas Views
- `ProjetoView` e `TarefaView` para formatar saída no console.

### Como usar no Console
1. Inicie o app: `python -m product_registrar.MVC.main`.
2. Escolha a opção `6. Projetos - Gerenciar` no menu principal.
3. Dentro do menu de projetos você pode:
   - Adicionar projetos
   - Listar projetos
   - Abrir um projeto (informando o ID) para gerenciar tarefas
4. Dentro de um projeto você pode:
   - Adicionar tarefa (opcionalmente informar status, padrão `pendente`)
   - Listar tarefas
   - Filtrar tarefas por status

### Exemplo de Status
Aceitos: `pendente`, `em_andamento`, `concluida`.
Se informar outro valor, um erro será exibido.

### Desafio Extra
O filtro por status foi implementado: dentro de um projeto escolha a opção "Filtrar tarefas por status" e informe o status.
