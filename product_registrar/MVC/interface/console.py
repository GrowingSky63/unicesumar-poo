from typing import Iterable
from ..controllers import ProdutoController, ProjetoController, TarefaController
from ..views import ProdutoView, ProjetoView, TarefaView


class ConsoleApp:
    """
    Interface principal usuário x console
    """

    def __init__(self) -> None:
        # Instanciando o controlador que gerencia as regras de negócio do app
        self.controller = ProdutoController()
        # Controladores de Projeto e Tarefa
        self.projeto_controller = ProjetoController()
        self.tarefa_controller = TarefaController(self.projeto_controller)
        # Instanciando as classes da view para visualizar as informações
        self.view = ProdutoView()
        self.projeto_view = ProjetoView()
        self.tarefa_view = TarefaView()
        # Define o tamanho em caracteres da interface no console
        self.view_width = 70

    def executar(self) -> None:
        """
        Método responsável pelo loop principal do app
        """
        while True:
            print(f"{'Sistema de Cadastro de Produtos e Projetos':-^{self.view_width}}")
            print("1. Adicionar produto")
            print("2. Listar produtos")
            print("3. Atualizar quantidade")
            print("4. Remover produto")
            print("5. Buscar por ID")
            print("6. Projetos - Gerenciar")
            print("0. Sair")
            print(f"{'':-^{self.view_width}}")
            with self._input(self.view_width):
                opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    self._adicionar()
                elif opcao == "2":
                    produto_view_list = self.view.listar_produtos(self.controller.listar_produtos())
                    self._output(produto_view_list)
                elif opcao == "3":
                    self._atualizar_quantidade()
                elif opcao == "4":
                    self._remover()
                elif opcao == "5":
                    self._buscar()
                elif opcao == "6":
                    self._menu_projetos()
                elif opcao == "0":
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida.")
            except ValueError as e:
                print(f"Erro: {e}")

    class _input:
        """
        Classe gerenciadora de contexto para entrada de dados em massa
        """
        def __init__(self, view_width: int):
            self.view_width = view_width

        def __enter__(self):
            # Ao entrar no contexto usando a palavra chave "with" do python, imprime "Entrada" centralizada com traços
            print(f"{'Entrada':-^{self.view_width}}")
            return self

        def __exit__(self, exc_type, exc, tb):
            # Ao sair do contexto (recuar uma identação), imprime os traços finais do bloco (com o tamanho da interface definido em self.view_width)
            print(f"{'':-^{self.view_width}}")
            return False

    def _output(self, message: str | Iterable) -> None:
        """
        Método para saída de dados
        """
        # Verifica se a mensagem é uma string, se sim, tenta separa por linhas
        if isinstance(message, str):
            message = message.split('\n')
        
        # Imprime Saída centralizado com traços
        print(f"{'Saída':-^{self.view_width}}")
        # Para cada linha da mensagem, a imprime centralizada, se for a última linha, remove a quebra de linha padrão do print
        [print(f"{m:^50}", end=None if i == len(message)-1 else '\n') for i, m in enumerate(message)]
        # Imprime os traços finais do bloco (com o tamanho da interface definido em self.view_width)
        print(f"{'':-^{self.view_width}}")

    def _adicionar(self) -> None:
        """
        Método responsável pela entrada de dados para a criação de um novo
        produto, mas que também, já o adiciona usando o controlador.
        """

        # Entrada de dados do usuário
        with self._input(self.view_width):
            id_str = input("ID: ").strip()
            nome = input("Nome: ").strip()
            preco_str = input("Preço: ").strip().replace(",", ".")
            qtd_str = input("Quantidade: ").strip()

        # Salva o produto no sistema e retorna a instancia do Produto criada
        produto = self.controller.adicionar_produto(
            id=int(id_str), nome=nome, preco=float(preco_str), quantidade=int(qtd_str)
        )

        # Mensagem de sucesso usando o atributo nome da entidade "Produto" no nosso formatador de saídas de dados para o usuário
        self._output(f"Produto '{produto.get_nome()}' adicionado com sucesso.")

    # ======== Projetos / Tarefas ========
    def _menu_projetos(self) -> None:
        while True:
            print(f"{'Projetos':-^{self.view_width}}")
            print("1. Adicionar projeto")
            print("2. Listar projetos")
            print("3. Abrir projeto por ID")
            print("0. Voltar")
            print(f"{'':-^{self.view_width}}")
            with self._input(self.view_width):
                opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    with self._input(self.view_width):
                        id_str = input("ID do projeto: ").strip()
                        nome = input("Nome do projeto: ").strip()
                    projeto = self.projeto_controller.adicionar_projeto(int(id_str), nome)
                    self._output(f"Projeto '{projeto.get_nome()}' adicionado com sucesso.")
                elif opcao == "2":
                    lista = self.projeto_view.listar_projetos(self.projeto_controller.listar_projetos())
                    self._output(lista)
                elif opcao == "3":
                    with self._input(self.view_width):
                        id_str = input("ID do projeto: ").strip()
                    self._menu_tarefas(int(id_str))
                elif opcao == "0":
                    break
                else:
                    print("Opção inválida.")
            except ValueError as e:
                print(f"Erro: {e}")

    def _menu_tarefas(self, projeto_id: int) -> None:
        projeto = self.projeto_controller.buscar_por_id(projeto_id)
        self._output(self.projeto_view.mostrar_projeto(projeto))
        if projeto is None:
            return
        while True:
            print(f"{'Tarefas do Projeto':-^{self.view_width}}")
            print("1. Adicionar tarefa")
            print("2. Listar tarefas")
            print("3. Filtrar tarefas por status")
            print("0. Voltar")
            print(f"{'':-^{self.view_width}}")
            with self._input(self.view_width):
                opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    with self._input(self.view_width):
                        descricao = input("Descrição: ").strip()
                        responsavel = input("Responsável: ").strip()
                        status = input("Status (pendente, em_andamento, concluida) [default pendente]: ").strip()
                        status = status or "pendente"
                    tarefa = self.tarefa_controller.adicionar_tarefa(projeto_id, descricao, responsavel, status)
                    self._output(f"Tarefa adicionada: {self.tarefa_view.mostrar_tarefa(tarefa)}")
                elif opcao == "2":
                    lista = self.tarefa_view.listar_tarefas(self.tarefa_controller.listar_tarefas(projeto_id))
                    self._output(lista)
                elif opcao == "3":
                    with self._input(self.view_width):
                        status = input("Status (pendente, em_andamento, concluida): ").strip()
                    lista = self.tarefa_view.listar_tarefas(self.tarefa_controller.filtrar_tarefas(projeto_id, status))
                    self._output(lista)
                elif opcao == "0":
                    break
                else:
                    print("Opção inválida.")
            except ValueError as e:
                print(f"Erro: {e}")

    def _atualizar_quantidade(self) -> None:
        """
        Método responsável pela entrada de dados para a atualização da
        quantidade, mas que também, já atualiza no sistema usando o controlador.
        """

        # Entrada de dados do usuário
        with self._input(self.view_width):
            id_str = input("ID do produto: ").strip()
            qtd_str = input("Nova quantidade: ").strip()

        # Atualiza o Produto no sistema e retorna True se exito, se não, False
        ok = self.controller.atualizar_quantidade(int(id_str), int(qtd_str))

        # Imprime mensagens de sucesso ou falha no nosso formatador de saídas de dados para o usuário
        if ok:
            self._output("Quantidade atualizada com sucesso.")
        else:
            self._output("Produto não encontrado.")

    def _remover(self) -> None:
        """
        Método responsável pela entrada de dados para a remoção de um Produto,
        mas que também, já remnove do sistema usando o controlador.
        """

        # Entrada de dados do usuário
        with self._input(self.view_width):
            id_str = input("ID do produto a remover: ").strip()

        # remove o Produto do sistema e retorna True se exito, se não, False
        ok = self.controller.remover_produto(int(id_str))

        # Imprime mensagens de sucesso ou falha no nosso formatador de saídas de dados para o usuário
        if ok:
            self._output("Produto removido com sucesso.")
        else:
            self._output("Produto não encontrado.")

    def _buscar(self) -> None:
        """
        Método responsável pela entrada de dados para a remoção de um Produto,
        mas que também, já remnove do sistema usando o controlador.
        """

        # Entrada de dados do usuário
        with self._input(self.view_width):
            id_str = input("ID do produto: ").strip()

        # Retorna a instancia do Produto
        produto = self.controller.buscar_por_id(int(id_str))

        # Retorna a visualização do produto
        produto_view = self.view.mostrar_produto(produto)

        # Imprime o produto no nosso formatador de saídas de dados para o usuário
        self._output(produto_view)


