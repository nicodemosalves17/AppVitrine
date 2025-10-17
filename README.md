# App de Gestão de Estoque e Controle de Vendas

Aplicativo Android feito em Python/Kivy para pequenas empresas com **menu hambúrguer lateral** moderno.

## Funcionalidades

- 🍔 **Menu hambúrguer lateral** com navegação intuitiva
- 📦 Cadastro, edição e exclusão de produtos
- 💰 Registro de vendas e compras com atualização automática do estoque
- 🗄️ Banco de dados local SQLite
- 🖼️ Imagem **anexada** obrigatoriamente para cada produto
- 👥 Sistema de usuários com permissões (admin/usuário)
- 📊 Relatórios detalhados com exportação para Excel/PDF
- 🔐 Login seguro com controle de acesso

## Novo Menu Hambúrguer

O aplicativo agora possui um menu lateral moderno que:
- Aparece após o login com o botão ☰
- Desliza suavemente da esquerda
- Fecha automaticamente após selecionar uma opção
- Adapta opções baseado em permissões (admin/usuário)

### Opções do Menu
- 🏠 **Vitrine** - Ver todos os produtos
- ➕ **Novo Produto** - Cadastrar produto (apenas admin)
- 👤 **Novo Usuário** - Cadastrar usuário (apenas admin)
- 📊 **Relatório** - Ver relatórios e estatísticas
- 🖼️ **Logo** - Alterar logo da empresa
- 🚪 **Sair** - Fazer logout

## Como rodar

1. Instale Python 3 e Kivy (`pip install kivy`).
2. Execute: `python main.py`
3. Para gerar APK, use [Buildozer](https://buildozer.readthedocs.io/en/latest/).

## Documentação

- 📚 **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - Guia rápido para usuários e desenvolvedores
- 🔧 **[MIGRACAO_MENU_HAMBURGER.md](MIGRACAO_MENU_HAMBURGER.md)** - Detalhes técnicos da implementação
- 📊 **[ESTRUTURA_VISUAL.md](ESTRUTURA_VISUAL.md)** - Diagramas e estrutura visual
- ✅ **[CONCLUSAO.md](CONCLUSAO.md)** - Resumo completo da migração

## Observações

- Use o botão "Selecionar Imagem" para anexar uma imagem do seu computador.
- O caminho da imagem ficará salvo no banco de dados e será exibido na vitrine e no popup.
- Para Android, use [plyer](https://github.com/kivy/plyer) para acesso à galeria/câmera.

## Estrutura do banco de dados

- **Código**
- **Nome**
- **Categoria**
- **Quantidade**
- **Preço**
- **Imagem** (obrigatória - caminho local)

## Login Padrão

Para testar o aplicativo, crie um usuário admin através do banco de dados ou pelo código.

## Estrutura do Projeto

```
AppVitrine/
├── main.py                 # Aplicação principal
├── db.py                   # Gerenciador de banco de dados
├── logo_manager.py         # Gerenciador de logo
├── root_layout.kv          # Layout raiz com menu hambúrguer
├── login.kv                # Tela de login
├── vitrine.kv              # Tela de produtos
├── cadastro.kv             # Tela de cadastro
├── popup.kv                # Tela de detalhes do produto
├── usuario.kv              # Tela de cadastro de usuários
├── relatorio.kv            # Tela de relatórios
└── produtos.db             # Banco de dados SQLite
```

## Tecnologias Utilizadas

- Python 3
- Kivy (Framework UI)
- SQLite (Banco de dados)
- Pandas (Exportação Excel)
- FPDF (Exportação PDF)

## Contribuindo

Pull requests são bem-vindos! Para grandes mudanças, por favor abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.