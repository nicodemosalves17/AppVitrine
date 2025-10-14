# Comportamento do Menu Hambúrguer

## Estados do Menu

### 1. Estado Inicial (Antes do Login)
```
┌─────────────────────────────────────┐
│                                     │  ← Botão hambúrguer INVISÍVEL
│                                     │
│         TELA DE LOGIN               │
│                                     │
│    [Usuário: _________]             │
│    [Senha:   _________]             │
│                                     │
│         [  ENTRAR  ]                │
│                                     │
└─────────────────────────────────────┘
```
**Estado dos botões:**
- Hambúrguer (☰): opacity=0, disabled=True
- Sair: opacity=0, disabled=True

---

### 2. Após Login Bem-Sucedido
```
┌─────────────────────────────────────┐
│ ☰                           [SAIR]  │  ← Botão hambúrguer VISÍVEL
│                                     │
│         TELA VITRINE                │
│                                     │
│   [Produto1] [Produto2] [Produto3]  │
│   [Produto4] [Produto5] [Produto6]  │
│                                     │
└─────────────────────────────────────┘
```
**Estado dos botões:**
- Hambúrguer (☰): opacity=1, disabled=False
- Sair: opacity=1, disabled=False

---

### 3. Menu Aberto
```
┌─────────────────────────────────────┐
│ ☰                           [SAIR]  │
│ ╔══════════════╗                    │
│ ║ MENU         ║  ░░░░░░░░░░░░░░░░  │ ← Overlay escuro
│ ╠══════════════╣  ░░░░░░░░░░░░░░░░  │
│ ║ NOVO PRODUTO ║  ░░░░░░░░░░░░░░░░  │
│ ║ NOVO USUÁRIO ║  ░░░░░░░░░░░░░░░░  │
│ ║ RELATÓRIO    ║  ░░░░░░░░░░░░░░░░  │
│ ║ LOGOMARCAR   ║  ░░░░░░░░░░░░░░░░  │
│ ║              ║  ░░░░░░░░░░░░░░░░  │
│ ║ [  Fechar  ] ║  ░░░░░░░░░░░░░░░░  │
│ ╚══════════════╝  ░░░░░░░░░░░░░░░░  │
└─────────────────────────────────────┘
```
**Características:**
- Menu desliza da esquerda (animação 0.3s)
- Overlay escuro semi-transparente (rgba: 0,0,0,0.5)
- Clicar no overlay fecha o menu
- Menu tem largura fixa de 250dp

---

### 4. Após Logout
```
┌─────────────────────────────────────┐
│                                     │  ← Volta ao estado inicial
│         TELA DE LOGIN               │
│                                     │
└─────────────────────────────────────┘
```
**Estado dos botões:**
- Hambúrguer (☰): opacity=0, disabled=True (voltou ao estado inicial)
- Sair: opacity=0, disabled=True

---

## Fluxo de Interação

### Abrindo o Menu
1. Usuário clica no botão hambúrguer (☰)
2. Método `root.abrir_menu()` é chamado
3. Propriedade `menu_aberto` muda para `True`
4. Menu desliza da posição x=-250dp para x=0 (0.3s, out_cubic)
5. Overlay aparece com fade-in

### Fechando o Menu
Três formas de fechar:

**A) Clicando no overlay:**
1. Usuário clica na área escura (overlay)
2. `on_touch_down` detecta o clique: `(root.menu_aberto and self.collide_point(*args[1].pos) and root.fechar_menu()) or False`
3. Método `root.fechar_menu()` é chamado
4. Menu desliza para x=-250dp (0.3s, out_cubic)
5. Overlay desaparece com fade-out

**B) Clicando no botão "Fechar":**
1. Usuário clica no botão "Fechar"
2. `root.fechar_menu()` é chamado diretamente
3. Mesmo efeito visual de (A)

**C) Selecionando uma opção do menu:**
1. Usuário clica em uma opção (ex: "NOVO PRODUTO")
2. `root.menu_action('cadastro')` é chamado
3. `fechar_menu()` é chamado primeiro
4. Menu fecha com animação
5. Depois navega para a tela selecionada

---

## Opções do Menu

### 1. NOVO PRODUTO
- **Ação:** Navega para a tela de cadastro de produto
- **Código:** `root.menu_action('cadastro')`
- **Implementação:** Limpa os campos e vai para 'cadastro'

### 2. NOVO USUÁRIO
- **Ação:** Navega para a tela de cadastro de usuário
- **Código:** `root.menu_action('usuario')`
- **Implementação:** Vai para 'usuario'

### 3. RELATÓRIO
- **Ação:** Navega para a tela de relatórios
- **Código:** `root.menu_action('relatorio')`
- **Implementação:** Vai para 'relatorio'

### 4. LOGOMARCAR
- **Ação:** Abre o seletor de logo
- **Código:** `root.menu_action('logomarcar')`
- **Implementação:** Chama `app.open_logo_chooser()` do LogoManager

---

## Detalhes Técnicos

### Animações
```python
# Abrir menu
anim = Animation(x=0, duration=0.3, t='out_cubic')
anim.start(side_menu)

# Fechar menu
anim = Animation(x=-dp(250), duration=0.3, t='out_cubic')
anim.start(side_menu)
```

### Propriedades Reativas
```python
menu_aberto = BooleanProperty(False)
```
Quando `menu_aberto` muda:
- Overlay: opacity muda entre 0 e 0.5
- Overlay: rgba muda dinamicamente
- Posição do menu: animada por código Python

### Overlay Touch Handler
```kv
on_touch_down: (root.menu_aberto and self.collide_point(*args[1].pos) and root.fechar_menu()) or False
```

**Explicação:**
1. `root.menu_aberto` - Verifica se menu está aberto
2. `self.collide_point(*args[1].pos)` - Verifica se clique foi no overlay
3. `root.fechar_menu()` - Fecha o menu (retorna True)
4. `or False` - Garante que sempre retorna False para não consumir o evento

---

## Controle de Visibilidade

### Método `habilitar_menu(habilitar=True)`
```python
if habilitar:
    btn_hamburger.opacity = 1
    btn_hamburger.disabled = False
    btn_sair.opacity = 1
    btn_sair.disabled = False
else:
    btn_hamburger.opacity = 0
    btn_hamburger.disabled = True
    btn_sair.opacity = 0
    btn_sair.disabled = True
    if self.menu_aberto:
        self.fechar_menu()
```

### Chamadas
- **LoginScreen.on_pre_enter():** `habilitar_menu(False)`
- **LoginScreen.login() [sucesso]:** `habilitar_menu(True)`
- **EstoqueApp.logout():** `habilitar_menu(False)`

---

## Estrutura de Layout

```
RootLayout (FloatLayout)
│
├── BoxLayout [main_content]
│   │
│   ├── BoxLayout [top_bar] height=48dp
│   │   ├── Button [btn_hamburger] "☰"
│   │   ├── Widget [spacer]
│   │   └── Button [btn_sair] "Sair"
│   │
│   └── BoxLayout [screen_container]
│       └── ScreenManager (adicionado em build())
│
├── BoxLayout [side_menu] width=250dp, x=-250dp ou 0
│   ├── Label "MENU"
│   ├── Widget (separator)
│   ├── Button "NOVO PRODUTO"
│   ├── Button "NOVO USUÁRIO"
│   ├── Button "RELATÓRIO"
│   ├── Button "LOGOMARCAR"
│   ├── Widget (spacer)
│   └── Button "Fechar"
│
└── Widget [overlay]
    └── opacity: 0.5 se menu_aberto, 0 caso contrário
```

---

## Compatibilidade

- ✅ Funciona em Desktop (Linux, Windows, macOS)
- ✅ Funciona em Mobile (Android via Buildozer)
- ✅ Touch e Mouse suportados
- ✅ Animações suaves em todas as plataformas
- ✅ Não interfere com outras telas existentes
