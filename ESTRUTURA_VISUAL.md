# Estrutura Visual - Menu Hambúrguer

## Hierarquia de Widgets

```
RootLayout (FloatLayout)
│
├── screen_manager_container (BoxLayout)
│   └── ScreenManager
│       ├── LoginScreen
│       ├── VitrineScreen
│       ├── CadastroScreen
│       ├── PopupScreen
│       ├── UsuarioScreen
│       └── RelatorioScreen
│
├── btn_hamburger (Button) - Posição: canto superior esquerdo
│   └── Texto: "☰"
│
├── overlay (Button) - Cobre toda tela quando menu aberto
│   └── Background: rgba(0, 0, 0, 0.5)
│
└── menu_lateral (BoxLayout) - Painel lateral 250dp
    ├── Header (BoxLayout)
    │   └── Label: "Menu"
    │
    └── Botões (BoxLayout vertical)
        ├── Button: "Vitrine"
        ├── Button: "Novo Produto" (admin only)
        ├── Button: "Novo Usuário" (admin only)
        ├── Button: "Relatório"
        ├── Button: "Logo"
        ├── Widget (spacer)
        └── Button: "Sair"
```

## Estados do Menu

### Estado 1: Login (Inicial)
```
┌─────────────────────────────┐
│                             │
│         LOGIN SCREEN        │
│                             │
│   [Usuario]                 │
│   [Senha]                   │
│   [Entrar]                  │
│                             │
│  btn_hamburger: OCULTO      │
│  menu_lateral: FECHADO      │
│                             │
└─────────────────────────────┘
```

### Estado 2: Após Login (Menu Fechado)
```
┌─────────────────────────────┐
│ ☰                           │ ← btn_hamburger visível
│                             │
│      VITRINE SCREEN         │
│                             │
│  [Produto1] [Produto2]      │
│  [Produto3] [Produto4]      │
│                             │
│  menu_lateral: FECHADO      │
│  (pos: -250dp)              │
└─────────────────────────────┘
```

### Estado 3: Menu Aberto
```
┌─────────────────────────────┐
│ ☰        ║                  │ ← Overlay semitransparente
│          ║                  │
│   MENU   ║   VITRINE        │
│          ║   (desfocado)    │
│ Vitrine  ║                  │
│ Novo Prod║   [Prod1] [Prod2]│
│ Novo User║                  │
│ Relatório║   [Prod3] [Prod4]│
│ Logo     ║                  │
│          ║                  │
│ Sair     ║                  │
└──────────╨──────────────────┘
     └── menu_lateral (pos: 0)
```

## Fluxo de Estados

```
┌──────────┐
│  Início  │
└────┬─────┘
     │
     v
┌─────────────┐
│ LoginScreen │ ← btn_hamburger: opacity=0, disabled=True
└────┬────────┘
     │ login()
     │ autenticado
     v
┌──────────────────┐
│ Mostra Hamburger │ ← btn_hamburger: opacity=1, disabled=False
└────┬─────────────┘
     │
     v
┌────────────────┐
│ VitrineScreen  │
└────┬───────────┘
     │
     v
┌───────────────────────────┐
│ Usuário pode:             │
│ 1. Clicar em ☰ → Abre menu│
│ 2. Menu → Navegar         │
│ 3. Menu → Sair            │
└────┬──────────────────────┘
     │
     ├─ [Clique em ☰]
     │       │
     │       v
     │  ┌──────────────┐
     │  │ Menu Aberto  │
     │  └──────┬───────┘
     │         │
     │         ├─ [Clique fora] → Fecha menu
     │         ├─ [Clique overlay] → Fecha menu
     │         ├─ [Escolhe tela] → Navega + Fecha menu
     │         └─ [Sair] → logout()
     │
     └─ [logout()]
            │
            v
     ┌──────────────────┐
     │ Oculta Hamburger │ ← btn_hamburger: opacity=0, disabled=True
     │ Fecha Menu       │ ← menu_aberto = False
     │ Volta ao Login   │ ← screen_manager.current = 'login'
     └──────────────────┘
```

## Propriedades Importantes

### RootLayout
- `menu_aberto` (BooleanProperty): Controla estado do menu
- `screen_manager`: Referência ao ScreenManager

### Posicionamento do Menu Lateral
```python
# Fechado
pos: (-dp(250), 0)  # Fora da tela à esquerda

# Aberto
pos: (0, 0)  # Alinhado à esquerda da tela
```

### Botão Hamburger
```python
# Login
opacity: 0
disabled: True

# Após Login
opacity: 1
disabled: False
```

## Animações (Sugeridas para Implementação Futura)

### Abrir Menu
```python
from kivy.animation import Animation

def toggle_menu(self, abrir):
    if abrir:
        anim = Animation(pos=(0, 0), duration=0.3, t='out_cubic')
        anim.start(self.ids.menu_lateral)
        self.menu_aberto = True
```

### Fechar Menu
```python
def fechar_menu(self):
    from kivy.metrics import dp
    anim = Animation(pos=(-dp(250), 0), duration=0.3, t='in_cubic')
    anim.start(self.ids.menu_lateral)
    self.menu_aberto = False
```

## Responsividade

### Desktop (Resolução Grande)
- Menu: 250dp (tamanho fixo)
- Conteúdo: Restante da tela

### Mobile (Resolução Pequena)
- Menu: 250dp ou 70% da largura (considerar ajustar)
- Conteúdo: Totalmente coberto quando menu aberto
- Overlay: Essencial para fechar menu facilmente

## Cores e Tema

### Paleta
- **Laranja Principal**: #ffa500 (rgba: 1, 0.647, 0, 1)
- **Menu Background**: #f2f2f2 (rgba: 0.95, 0.95, 0.95, 1)
- **Overlay**: rgba(0, 0, 0, 0.5)

### Aplicação
- Background geral: Laranja (#ffa500)
- Menu lateral: Cinza claro (#f2f2f2)
- Header do menu: Laranja (#ffa500)
