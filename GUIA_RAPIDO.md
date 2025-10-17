# 🍔 Guia Rápido - Menu Hambúrguer

## Para Usuários

### Como Usar o Novo Menu

#### 1. Login
- Abra o aplicativo
- Digite seu usuário e senha
- Clique em "Entrar"
- O botão ☰ aparecerá no canto superior esquerdo

#### 2. Acessar o Menu
- Clique no botão ☰
- O menu deslizará da esquerda
- Escolha uma opção

#### 3. Opções do Menu

**Todos os usuários:**
- 🏠 **Vitrine** - Ver produtos
- 📊 **Relatório** - Ver relatórios e estatísticas
- 🖼️ **Logo** - Alterar logo da empresa
- 🚪 **Sair** - Fazer logout

**Apenas Administradores:**
- ➕ **Novo Produto** - Cadastrar produto
- 👤 **Novo Usuário** - Cadastrar usuário

#### 4. Fechar o Menu
- Clique em uma opção (fecha automaticamente)
- Clique fora do menu (na área escura)
- Clique novamente em ☰

#### 5. Logout
- Abra o menu
- Clique em "Sair"
- Você voltará à tela de login
- O botão ☰ desaparecerá

## Para Desenvolvedores

### Estrutura Rápida

```python
# Estrutura da aplicação
RootLayout (root)
├── screen_manager (ScreenManager)
│   ├── login
│   ├── vitrine
│   ├── cadastro
│   ├── popup
│   ├── usuario
│   └── relatorio
├── btn_hamburger (Button ☰)
├── overlay (transparente)
└── menu_lateral (painel 250dp)
```

### Comandos Úteis

```python
# Navegar para uma tela
app.ir_para('vitrine')

# Abrir/fechar menu
app.root.menu_aberto = True
app.root.menu_aberto = False

# Debug
app.print_debug()

# Mostrar/ocultar hamburger
app.root.ids.btn_hamburger.opacity = 1  # mostrar
app.root.ids.btn_hamburger.opacity = 0  # ocultar
```

### Propriedades Importantes

```python
# RootLayout
root.menu_aberto          # bool - Estado do menu
root.screen_manager       # ScreenManager - Gerenciador de telas

# EstoqueApp
app.is_admin              # bool - Usuário é admin?
app.logo_path             # str - Caminho da logo
```

### Métodos Principais

```python
# RootLayout
root.navegar(tela)        # Navega e fecha menu
root.toggle_menu(abrir)   # Abre/fecha menu
root.fechar_menu()        # Fecha menu
root.abrir_logo()         # Abre seletor de logo

# EstoqueApp
app.ir_para(tela)         # Navega para tela (com debug)
app.print_debug()         # Imprime info de debug
app.logout()              # Faz logout completo
```

## Testes Rápidos

### Teste 1: Login e Menu
```
1. Execute: python main.py
2. Faça login
3. Verifique se ☰ aparece
4. Clique em ☰
5. Verifique se menu abre
```

### Teste 2: Navegação
```
1. Abra o menu
2. Clique em "Vitrine"
3. Verifique se vai para vitrine
4. Verifique se menu fecha
```

### Teste 3: Permissões
```
1. Login como usuário normal
2. Abra o menu
3. Verifique se "Novo Produto" está desabilitado
4. Logout e login como admin
5. Verifique se agora está habilitado
```

### Teste 4: Logout
```
1. Estando logado, clique em "Sair"
2. Verifique se volta ao login
3. Verifique se ☰ desaparece
```

## Troubleshooting

### Problema: Menu não abre
**Solução:**
- Verifique se está logado
- Verifique se `app.root.menu_aberto` está sendo atualizado
- Execute `app.print_debug()` para verificar estrutura

### Problema: Botão ☰ não aparece após login
**Solução:**
```python
# No código após login bem-sucedido:
app.root.ids.btn_hamburger.opacity = 1
app.root.ids.btn_hamburger.disabled = False
```

### Problema: Navegação não funciona
**Solução:**
- Verifique se `root.screen_manager` está definido
- Verifique se o nome da tela está correto
- Use `app.print_debug()` para ver telas disponíveis

### Problema: Menu não fecha
**Solução:**
```python
# Forçar fechamento:
app.root.menu_aberto = False
```

## Arquivos Importantes

### Código Principal
- `main.py` - Aplicação principal
- `root_layout.kv` - Layout do menu

### Telas
- `login.kv`
- `vitrine.kv`
- `cadastro.kv`
- `popup.kv`
- `usuario.kv`
- `relatorio.kv`

### Documentação
- `MIGRACAO_MENU_HAMBURGER.md` - Detalhes técnicos
- `ESTRUTURA_VISUAL.md` - Diagramas
- `CONCLUSAO.md` - Resumo completo
- `GUIA_RAPIDO.md` - Este arquivo

## Cores e Tema

- **Laranja Principal:** #ffa500 (rgba: 1, 0.647, 0, 1)
- **Menu Background:** #f2f2f2 (rgba: 0.95, 0.95, 0.95, 1)
- **Overlay:** rgba(0, 0, 0, 0.5)

## Tamanhos

- **Menu Lateral:** 250dp
- **Botão Hambúrguer:** 48x48 dp
- **Botões do Menu:** 48dp altura

## Fluxograma Simplificado

```
Login → [☰ aparece] → Clique em ☰ → Menu abre
                                   ↓
                              Escolhe opção
                                   ↓
                            Tela muda + Menu fecha
                                   ↓
                            [☰] → Repete processo
                            [Sair] → Volta ao Login
```

## Atalhos de Desenvolvimento

### Ver todas as telas
```python
print(app.root.screen_manager.screen_names)
# Output: ['login', 'vitrine', 'cadastro', 'popup', 'usuario', 'relatorio']
```

### Ver tela atual
```python
print(app.root.screen_manager.current)
```

### Verificar se é admin
```python
print(app.is_admin)
```

### Estado do menu
```python
print(app.root.menu_aberto)
```

## Suporte

Para dúvidas ou problemas:
1. Consulte `MIGRACAO_MENU_HAMBURGER.md` para detalhes técnicos
2. Consulte `ESTRUTURA_VISUAL.md` para entender a estrutura
3. Use `app.print_debug()` para diagnóstico
4. Verifique os logs de erro no console

---

**Versão:** 1.0  
**Data:** 2025-10-17  
**Branch:** copilot/update-hamburger-menu-migration
