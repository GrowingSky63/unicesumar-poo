from flask import Flask, jsonify, request, abort, render_template
from datetime import datetime
import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from infraestructure.database import init_db
from infraestructure.repositories.livro_sqlite_repository import LivroReceitasSQLiteRepository
from domain.entities.livro_receitas import LivroReceitas
from domain.entities.receita import Receita
from domain.entities.categoria import Categoria
from domain.entities.ingrediente import Ingrediente
from domain.value_objects.autor import Autor
from domain.value_objects.quantidade import Quantidade
from api.schemas import livro_to_dict, receita_to_dict, categoria_to_dict, ingrediente_to_dict
from domain.value_objects.quantidade import COOKING_UNITS

app = Flask(__name__)
init_db()
repo = LivroReceitasSQLiteRepository()


@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp

@app.route('/<path:_any>', methods=['OPTIONS'])
@app.route('/', methods=['OPTIONS'])
def options(_any=None):
    return '', 204

# --- Helper functions ---

def _get_livro_or_404(livro_id: str) -> LivroReceitas:
    livro = repo.get(livro_id)
    if not livro:
        abort(404, description='Livro não encontrado')
    return livro

def _get_categoria_or_404(livro: LivroReceitas, categoria_id: str) -> Categoria:
    cat = next((c for c in livro.categorias if c.id == categoria_id), None)
    if not cat:
        abort(404, description='Categoria não encontrada')
    return cat

def _get_receita_or_404(livro: LivroReceitas, receita_id: str) -> Receita:
    rec = next((r for r in livro.receitas if r.id == receita_id), None)
    if not rec:
        abort(404, description='Receita não encontrada')
    return rec

# --- Livro endpoints ---
@app.post('/livros')
def create_livro():
    data = request.json or {}
    try:
        titulo = data['titulo']
        autor = Autor(data['autor'])
    except KeyError as e:
        abort(400, description=f'Campo obrigatório ausente: {e.args[0]}')
    livro = LivroReceitas(titulo=titulo, autor=autor, data_criacao=datetime.now())
    repo.add(livro)
    return jsonify(livro_to_dict(livro)), 201

@app.get('/')
def home():
    return render_template('index.html')

@app.put('/livros/<livro_id>')
def update_livro(livro_id):
    livro = _get_livro_or_404(livro_id)
    data = request.json or {}
    if 'titulo' in data:
        livro.titulo = data['titulo']
    if 'autor' in data:
        try:
            livro.autor = Autor(data['autor'])
        except Exception as e:
            abort(400, description=f'Autor inválido: {e}')
    repo.update(livro)
    return jsonify(livro_to_dict(livro))

@app.get('/livros')
def list_livros():
    return jsonify([livro_to_dict(l) for l in repo.list()])

@app.get('/livros/<livro_id>')
def get_livro(livro_id):
    livro = _get_livro_or_404(livro_id)
    return jsonify(livro_to_dict(livro))

@app.delete('/livros/<livro_id>')
def delete_livro(livro_id):
    _get_livro_or_404(livro_id)
    repo.remove(livro_id)
    return '', 204

# --- Categoria endpoints ---
@app.post('/livros/<livro_id>/categorias')
def add_categoria(livro_id):
    livro = _get_livro_or_404(livro_id)
    data = request.json or {}
    nome = data.get('nome')
    if not nome:
        abort(400, description='Nome é obrigatório')
    descricao = data.get('descricao', '')
    cat = Categoria(nome=nome, descricao=descricao)
    livro.categorias.append(cat)
    repo.update(livro)
    return jsonify(categoria_to_dict(cat)), 201

@app.get('/livros/<livro_id>/categorias/<categoria_id>')
def get_categoria(livro_id, categoria_id):
    livro = _get_livro_or_404(livro_id)
    cat = _get_categoria_or_404(livro, categoria_id)
    return jsonify(categoria_to_dict(cat))

@app.put('/livros/<livro_id>/categorias/<categoria_id>')
def update_categoria(livro_id, categoria_id):
    livro = _get_livro_or_404(livro_id)
    cat = _get_categoria_or_404(livro, categoria_id)
    data = request.json or {}
    if 'nome' in data:
        cat.nome = data['nome']
    if 'descricao' in data:
        cat.descricao = data['descricao']
    repo.update(livro)
    return jsonify(categoria_to_dict(cat))

@app.delete('/livros/<livro_id>/categorias/<categoria_id>')
def delete_categoria(livro_id, categoria_id):
    livro = _get_livro_or_404(livro_id)
    cat = _get_categoria_or_404(livro, categoria_id)
    livro.categorias = [c for c in livro.categorias if c.id != categoria_id]
    repo.update(livro)
    return '', 204

@app.get('/livros/<livro_id>/categorias')
def list_categorias(livro_id):
    livro = _get_livro_or_404(livro_id)
    return jsonify([categoria_to_dict(c) for c in livro.categorias])

# --- Receita endpoints ---
@app.post('/livros/<livro_id>/receitas')
def add_receita(livro_id):
    livro = _get_livro_or_404(livro_id)
    data = request.json or {}
    required = ['nome', 'tempo_preparo', 'rendimento', 'modo_preparo']
    if not all(k in data for k in required):
        abort(400, description=f'Campos obrigatórios: {required}')
    categoria_id = request.args.get('categoria_id') or data.get('categoria_id')
    ingredientes_payload = data.get('ingredientes', [])
    ingredientes = []
    for ing in ingredientes_payload:
        try:
            nome_ing = ing['nome']
            qtd_raw = ing['quantidade']
            quantidade = Quantidade.from_string(qtd_raw) if isinstance(qtd_raw, str) else Quantidade(qtd_raw['valor'], qtd_raw['unidade'])
        except Exception as e:
            abort(400, description=f'Ingrediente inválido: {e}')
        ingredientes.append(Ingrediente(nome=nome_ing, quantidade=quantidade))
    receita = Receita(
        nome=data['nome'],
        tempo_preparo=float(data['tempo_preparo']),
        rendimento=data['rendimento'],
        modo_preparo=data['modo_preparo'],
        ingredientes=ingredientes
    )
    livro.receitas.append(receita)
    if categoria_id:
        categoria = next((c for c in livro.categorias if c.id == categoria_id), None)
        if not categoria:
            abort(404, description='Categoria informada não encontrada')
        if receita not in categoria.receitas:
            categoria.receitas.append(receita)
    repo.update(livro)
    payload = receita_to_dict(receita)
    if categoria_id:
        payload['categoria_id'] = categoria_id
    return jsonify(payload), 201

@app.get('/livros/<livro_id>/receitas')
def list_receitas(livro_id):
    livro = _get_livro_or_404(livro_id)
    return jsonify([receita_to_dict(r) for r in livro.receitas])

@app.get('/livros/<livro_id>/receitas/<receita_id>')
def get_receita(livro_id, receita_id):
    livro = _get_livro_or_404(livro_id)
    rec = _get_receita_or_404(livro, receita_id)
    return jsonify(receita_to_dict(rec))

@app.put('/livros/<livro_id>/receitas/<receita_id>')
def update_receita(livro_id, receita_id):
    livro = _get_livro_or_404(livro_id)
    rec = _get_receita_or_404(livro, receita_id)
    data = request.json or {}
    if 'nome' in data:
        rec.nome = data['nome']
    if 'tempo_preparo' in data:
        rec.tempo_preparo = float(data['tempo_preparo'])
    if 'rendimento' in data:
        rec.rendimento = data['rendimento']
    if 'modo_preparo' in data:
        rec.modo_preparo = data['modo_preparo']
    if 'ingredientes' in data:
        novos = []
        for ing in data['ingredientes']:
            nome_ing = ing.get('nome')
            qtd_raw = ing.get('quantidade')
            if not nome_ing or not qtd_raw:
                abort(400, description='Ingrediente inválido (nome/quantidade)')
            quantidade = Quantidade.from_string(qtd_raw) if isinstance(qtd_raw, str) else Quantidade(qtd_raw['valor'], qtd_raw['unidade'])
            novos.append(Ingrediente(nome=nome_ing, quantidade=quantidade))
        rec.ingredientes = novos
    repo.update(livro)
    return jsonify(receita_to_dict(rec))

@app.delete('/livros/<livro_id>/receitas/<receita_id>')
def delete_receita(livro_id, receita_id):
    livro = _get_livro_or_404(livro_id)
    _ = _get_receita_or_404(livro, receita_id)
    livro.receitas = [r for r in livro.receitas if r.id != receita_id]
    for c in livro.categorias:
        c.receitas = [r for r in c.receitas if r.id != receita_id]
    repo.update(livro)
    return '', 204

# --- Ingredientes / Unidades ---
@app.get('/livros/<livro_id>/ingredientes')
def list_ingredientes(livro_id):
    livro = _get_livro_or_404(livro_id)
    nomes = []
    seen = set()
    for r in livro.receitas:
        for ing in r.ingredientes:
            if ing.nome not in seen:
                seen.add(ing.nome)
                nomes.append(ing.nome)
    return jsonify({'ingredientes': nomes})

@app.get('/unidades')
def list_unidades():
    return jsonify({'unidades': sorted(COOKING_UNITS)})

@app.post('/livros/<livro_id>/categorias/<categoria_id>/receitas/<receita_id>')
def link_receita_categoria(livro_id, categoria_id, receita_id):
    livro = _get_livro_or_404(livro_id)
    categoria = next((c for c in livro.categorias if c.id == categoria_id), None)
    receita = next((r for r in livro.receitas if r.id == receita_id), None)
    if not categoria or not receita:
        abort(404, description='Categoria ou Receita não encontrada')
    if receita not in categoria.receitas:
        categoria.receitas.append(receita)
        repo.update(livro)
    return jsonify(categoria_to_dict(categoria))

if __name__ == '__main__':
    app.run(debug=True)
