# App de Gestão de Estoque e Controle de Vendas

Aplicativo Android feito em Python/Kivy para pequenas empresas.

## Estrutura do Projeto

O projeto foi organizado em uma estrutura modular para facilitar manutenção e desenvolvimento:

```
AppVitrine/
├── main.py                    # Entrada principal da aplicação
├── buildozer.spec            # Configuração para build Android
├── src/                      # Código fonte principal
│   ├── __init__.py
│   ├── components.py         # Componentes reutilizáveis
│   ├── models/               # Modelos de dados e acesso ao BD
│   │   ├── __init__.py
│   │   └── db.py
│   ├── managers/             # Managers e mixins
│   │   ├── __init__.py
│   │   ├── logo_manager.py
│   │   └── menu_manager.py
│   └── screens/              # Telas da aplicação
│       ├── __init__.py
│       ├── base_screen.py
│       ├── login_screen.py
│       ├── vitrine_screen.py
│       ├── cadastro_screen.py
│       ├── popup_screen.py
│       ├── usuario_screen.py
│       └── relatorio_screen.py
├── ui/                       # Arquivos de interface (KV)
│   ├── base_template.kv
│   ├── base_template_with_menu.kv
│   ├── menu.kv
│   ├── login.kv
│   ├── vitrine.kv
│   ├── cadastro.kv
│   ├── popup.kv
│   ├── usuario.kv
│   └── relatorio.kv
├── assets/                   # Recursos estáticos
│   ├── logo_empresa.png
│   ├── produtos.db
│   └── relatorio_historico.xlsx
└── docs/                     # Documentação
    ├── README.md
    └── INSTRUCOES_MENU.md
```

## Funcionalidades

- Cadastro, edição e exclusão de produtos
- Registro de vendas e compras com atualização automática do estoque
- Banco de dados local SQLite
- Imagem **anexada** obrigatoriamente para cada produto
- Sistema de usuários com controle de acesso (admin/usuário)
- Menu contextual com funcionalidades administrativas
- Relatórios de estoque e histórico de movimentações

## Como rodar

1. Instale Python 3 e Kivy (`pip install kivy`).
2. Execute: `python main.py`
3. Para gerar APK, use [Buildozer](https://buildozer.readthedocs.io/en/latest/).

## Observações

- Use o botão "Selecionar Imagem" para anexar uma imagem do seu computador.
- O caminho da imagem ficará salvo no banco de dados e será exibido na vitrine e no popup.
- Para Android, use [plyer](https://github.com/kivy/plyer) para acesso à galeria/câmera.
- Login padrão: usuário `admin`, senha `admin`

## Estrutura do banco de dados

### Tabela: produtos
- **Código** (TEXT, PRIMARY KEY)
- **Nome** (TEXT)
- **Categoria** (TEXT)
- **Quantidade** (INTEGER)
- **Preço** (REAL)
- **Imagem** (TEXT - caminho local)

### Tabela: usuários
- **ID** (INTEGER, AUTOINCREMENT)
- **Usuário** (TEXT, UNIQUE)
- **Senha** (TEXT)
- **Perfil** (TEXT: 'admin' ou 'usuario')

### Tabela: histórico
- **ID** (INTEGER, AUTOINCREMENT)
- **Produto Código** (TEXT)
- **Produto Nome** (TEXT)
- **Produto Categoria** (TEXT)
- **Quantidade** (INTEGER)
- **Tipo** (TEXT: 'venda' ou 'compra')
- **Data/Hora** (TEXT)
- **Usuário** (TEXT)