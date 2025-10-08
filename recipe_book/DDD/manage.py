import argparse
import sys
from pathlib import Path

# Ajustar path para imports relativos funcionarem ao executar diretamente
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))

def cmd_runserver(host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
    from api.app import app  # lazy import para evitar custo em outros comandos
    app.run(host=host, port=port, debug=debug)

def cmd_runtests():
    """Executa testes simples (script tests/main.py). Retorna código 0 se sem exceções críticas."""
    import runpy
    test_path = BASE_DIR / 'tests' / 'main.py'
    if not test_path.exists():
        print('Arquivo de testes não encontrado:', test_path)
        return 1
    try:
        runpy.run_path(str(test_path), run_name='__main__')
        print('\n[TESTS] Finalizado.')
        return 0
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 1
    except Exception as e:
        print('[TESTS] Falhou com exceção:', e)
        return 1

def build_parser():
    parser = argparse.ArgumentParser(description='Gerenciador da aplicação Livro de Receitas')
    sub = parser.add_subparsers(dest='command', required=True)

    p_run = sub.add_parser('runserver', help='Inicia a API Flask')
    p_run.add_argument('--host', default='127.0.0.1')
    p_run.add_argument('--port', type=int, default=5000)
    p_run.add_argument('--no-debug', action='store_true', help='Desativa modo debug')

    sub.add_parser('runtests', help='Executa testes simples')
    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == 'runserver':
        debug = not args.no_debug
        cmd_runserver(host=args.host, port=args.port, debug=debug)
    elif args.command == 'runtests':
        code = cmd_runtests()
        sys.exit(code)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
