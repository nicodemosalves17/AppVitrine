# Quick Start - Menu Hambúrguer

## Para Desenvolvedores

Se você é novo no projeto ou está retornando após a migração, aqui está tudo que você precisa saber sobre o novo menu hambúrguer.

## O que mudou?

### ❌ Removido (NÃO USE MAIS):
- `menu.kv` - Arquivo deletado
- `base_template.kv` - Arquivo deletado  
- `base_template_with_menu.kv` - Arquivo deletado
- `MenuManager` - Não é mais herdado pela App
- `show_top_menu` - Propriedade removida
- `TopMenu` - Widget removido

### ✅ Novo (USE ISTO):
- `root_layout.kv` - Layout raiz com menu hambúrguer
- `root_layout.py` - Classe RootLayout
- `RootLayout` - Widget principal que contém o menu

## Como usar o menu?

### No código Python:

```python
# Para controlar visibilidade do menu:
app = App.get_running_app()

# Mostrar o menu (após login)
app.root_layout.habilitar_menu(True)

# Ocultar o menu (antes login, após logout)
app.root_layout.habilitar_menu(False)

# Abrir o menu programaticamente (raramente necessário)
app.root_layout.abrir_menu()

# Fechar o menu programaticamente (raramente necessário)
app.root_layout.fechar_menu()
```

### Adicionar nova opção ao menu:

1. Abra `root_layout.kv`
2. Adicione um novo Button na seção de opções:
```kv
Button:
    text: "NOVA OPÇÃO"
    size_hint_y: None
    height: dp(50)
    on_release: root.menu_action('nova_opcao')
```

3. Abra `root_layout.py`
4. Adicione o handler no método `menu_action`:
```python
elif action == 'nova_opcao':
    try:
        app.root.current = 'nome_da_tela'
    except Exception as e:
        print(f"Erro ao navegar: {e}")
```

## Estrutura do Projeto

```
AppVitrine/
├── root_layout.kv        ← Layout do menu hambúrguer
├── root_layout.py        ← Lógica do menu hambúrguer
├── main.py               ← App principal (usa RootLayout)
├── login.kv              ← Tela de login
├── vitrine.kv            ← Tela de produtos
├── cadastro.kv           ← Tela de cadastro
├── popup.kv              ← Detalhes do produto
├── usuario.kv            ← Cadastro de usuário
├── relatorio.kv          ← Relatórios
├── logo_manager.py       ← Gerenciador de logo
└── db.py                 ← Banco de dados
```

## Como o menu funciona?

### Estado Inicial (Login)
```
Menu: INVISÍVEL
Botão hambúrguer: opacity=0, disabled=True
```

### Após Login
```
Menu: VISÍVEL
Botão hambúrguer: opacity=1, disabled=False
Usuario pode clicar em ☰ para abrir o menu
```

### Menu Aberto
```
Menu desliza da esquerda
Overlay escuro aparece
Usuario pode:
  - Clicar em uma opção → Navega + fecha menu
  - Clicar no overlay → Fecha menu
  - Clicar em "Fechar" → Fecha menu
```

### Após Logout
```
Menu: INVISÍVEL (volta ao estado inicial)
```

## Debugging

### Menu não aparece após login?
```python
# Verifique se está chamando:
app.root_layout.habilitar_menu(True)
```

### Menu não fecha?
```python
# Verifique se menu_aberto está sendo atualizado:
print(f"Menu aberto: {app.root_layout.menu_aberto}")
```

### Animação não funciona?
```python
# Verifique se Animation está importado:
from kivy.animation import Animation
```

### Erro ao navegar?
```python
# Verifique se a tela existe no ScreenManager:
print(app.root.screen_names)
```

## Documentação Completa

- **MIGRATION_SUMMARY.md** - Detalhes técnicos da migração
- **MENU_BEHAVIOR.md** - Comportamento visual com diagramas
- **QUICK_START.md** - Este arquivo (início rápido)

## Perguntas Frequentes

**Q: Posso customizar o menu?**  
A: Sim! Edite `root_layout.kv` para mudar cores, tamanhos, espaçamentos.

**Q: Posso mudar o ícone hambúrguer?**  
A: Sim! Em `root_layout.kv`, linha ~29, mude `text: "☰"` para outro ícone.

**Q: Como adicionar uma animação diferente?**  
A: Edite `root_layout.py`, métodos `abrir_menu()` e `fechar_menu()`.

**Q: O menu funciona em mobile?**  
A: Sim! Testado com Buildozer para Android.

**Q: Preciso fazer algo nas telas existentes?**  
A: Não! Todas as telas continuam funcionando sem modificação.

**Q: E se eu quiser um menu no topo ao invés de lateral?**  
A: Você pode criar um novo layout baseado em `root_layout.kv` com o menu posicionado no topo.

## Suporte

Se tiver dúvidas:
1. Leia MIGRATION_SUMMARY.md para detalhes técnicos
2. Leia MENU_BEHAVIOR.md para entender o comportamento
3. Veja o código em root_layout.py (bem comentado)
4. Teste localmente com `python main.py`

## Contribuindo

Ao adicionar funcionalidades:
1. Mantenha o padrão de código existente
2. Adicione try/except para robustez
3. Teste com e sem login
4. Verifique animações em mobile
5. Atualize documentação se necessário

---

**Última atualização:** Após migração completa para menu hambúrguer  
**Status:** ✅ Pronto para uso
