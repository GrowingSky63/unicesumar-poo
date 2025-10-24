#!/usr/bin/env python
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INNER = ROOT / 'livro_receitas' / 'DDD' / 'manage.py'

if not INNER.exists():
    print('Erro: manage.py interno não encontrado em', INNER, file=sys.stderr)
    sys.exit(1)

# Executa o manage.py interno preservando __main__
runpy.run_path(str(INNER), run_name='__main__')
