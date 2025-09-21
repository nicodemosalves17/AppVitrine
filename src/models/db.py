import sqlite3

class BancoDados:
    @staticmethod
    def conectar():
        return sqlite3.connect("produtos.db")

    @staticmethod
    def criar_tabela():
        conn = BancoDados.conectar()
        c = conn.cursor()
        # Produtos
        c.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                codigo TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                imagem TEXT NOT NULL
            )
        ''')
        # Usuários
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL CHECK(perfil IN ('admin', 'usuario'))
            )
        ''')
        # Histórico
        c.execute('''
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_codigo TEXT NOT NULL,
                produto_nome TEXT NOT NULL,
                produto_categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('venda', 'compra')),
                datahora TEXT NOT NULL,
                usuario TEXT NOT NULL
            )
        ''')
        # Cria admin padrão, se não existir
        c.execute('SELECT * FROM usuarios WHERE usuario = ?', ('admin',))
        if not c.fetchone():
            c.execute('INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)', ('admin', 'admin', 'admin'))
        conn.commit()
        conn.close()

    @staticmethod
    def autenticar(usuario, senha):
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('SELECT perfil FROM usuarios WHERE usuario=? AND senha=?', (usuario, senha))
        row = c.fetchone()
        conn.close()
        if row:
            return row[0]
        return None

    @staticmethod
    def cadastrar_usuario(usuario, senha, perfil):
        conn = BancoDados.conectar()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)', (usuario, senha, perfil))
            conn.commit()
            conn.close()
            return True, ""
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Usuário já existe!"

    @staticmethod
    def cadastrar_produto(produto):
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO produtos (codigo, nome, categoria, quantidade, preco, imagem)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (produto["codigo"], produto["nome"], produto["categoria"], produto["quantidade"], produto["preco"], produto["imagem"]))
        conn.commit()
        conn.close()

    @staticmethod
    def obter_todos_produtos():
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('SELECT * FROM produtos')
        resultado = c.fetchall()
        conn.close()
        produtos = []
        for row in resultado:
            produtos.append({
                "codigo": row[0],
                "nome": row[1],
                "categoria": row[2],
                "quantidade": row[3],
                "preco": row[4],
                "imagem": row[5]
            })
        return produtos

    @staticmethod
    def obter_produto(codigo):
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('SELECT * FROM produtos WHERE codigo=?', (codigo,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "codigo": row[0],
                "nome": row[1],
                "categoria": row[2],
                "quantidade": row[3],
                "preco": row[4],
                "imagem": row[5]
            }
        return None

    @staticmethod
    def excluir_produto(codigo):
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('DELETE FROM produtos WHERE codigo=?', (codigo,))
        conn.commit()
        conn.close()

    @staticmethod
    def atualizar_estoque(codigo, nova_quantidade):
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('UPDATE produtos SET quantidade=? WHERE codigo=?', (nova_quantidade, codigo))
        conn.commit()
        conn.close()

    @staticmethod
    def registrar_operacao(produto, quantidade, tipo, usuario):
        import datetime
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('''
            INSERT INTO historico (produto_codigo, produto_nome, produto_categoria, quantidade, tipo, datahora, usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (produto['codigo'], produto['nome'], produto['categoria'], quantidade, tipo, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), usuario))
        conn.commit()
        conn.close()

    @staticmethod
    def obter_historico():
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('SELECT produto_codigo, produto_nome, produto_categoria, tipo, datahora, usuario FROM historico ORDER BY datahora DESC')
        historico = c.fetchall()
        conn.close()
        return historico

    @staticmethod
    def produtos_mais_movimentados(limit=10):
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('''
            SELECT produto_nome, SUM(CASE WHEN tipo='venda' THEN quantidade ELSE 0 END) AS vendido,
                                SUM(CASE WHEN tipo='compra' THEN quantidade ELSE 0 END) AS comprado
            FROM historico
            GROUP BY produto_nome
            ORDER BY vendido DESC, comprado DESC
            LIMIT ?
        ''', (limit,))
        data = c.fetchall()
        conn.close()
        return data

    @staticmethod
    def relatorio_estoque():
        conn = BancoDados.conectar()
        c = conn.cursor()
        c.execute('''
            SELECT
                p.codigo,
                p.nome,
                p.categoria,
                COALESCE(SUM(CASE WHEN h.tipo='compra' THEN h.quantidade END), 0) AS total_compra,
                COALESCE(SUM(CASE WHEN h.tipo='venda' THEN h.quantidade END), 0) AS total_venda,
                p.quantidade as estoque
            FROM produtos p
            LEFT JOIN historico h ON p.codigo = h.produto_codigo
            GROUP BY p.codigo, p.nome, p.categoria, p.quantidade
            ORDER BY p.nome
        ''')
        dados = c.fetchall()
        conn.close()
        return dados