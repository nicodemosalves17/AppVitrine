# Migração Completa para Menu Hambúrguer

## Resumo das Mudanças

Este documento descreve a migração completa do antigo sistema de menu (TopMenu) para o novo menu hambúrguer lateral.

## Arquivos Removidos

1. **menu.kv** - Menu antigo com botão "Menu ▾"
2. **base_template.kv** - Template base que incluía o TopMenu
3. **base_template_with_menu.kv** - Template alternativo com menu

## Arquivos Criados

1. **root_layout.kv** - Layout raiz com menu hambúrguer lateral
   - Menu desliza da esquerda para a direita com animação
   - Overlay escuro quando menu está aberto
   - Usa expressão de linha única para on_touch_down no overlay
   - Botão hambúrguer (☰) invisível e desabilitado antes do login

2. **root_layout.py** - Classe RootLayout
   - Gerencia estado do menu (aberto/fechado)
   - Controla animações de entrada/saída do menu
   - Método `habilitar_menu()` para mostrar/ocultar botão
   - Métodos para cada ação do menu (cadastro, usuário, relatório, logomarcar)

## Arquivos Modificados

### main.py

#### Imports
- Removido: `from menu_manager import MenuManager`
- Adicionado: `from root_layout import RootLayout`

#### Carregamento de templates
- Removido: Carregamento de `base_template.kv` e `menu.kv`
- Adicionado: Carregamento de `root_layout.kv`

#### Classe EstoqueApp
- Removida herança de `MenuManager`
- Removida propriedade `show_top_menu`
- Método `build()` atualizado para:
  - Criar instância de RootLayout
  - Adicionar ScreenManager ao container do RootLayout
  - Retornar RootLayout como raiz da aplicação
- Método `logout()` atualizado para ocultar menu hambúrguer

#### Screens
Removidas todas as referências a `show_top_menu` das seguintes telas:
- **LoginScreen**: 
  - `on_pre_enter()` - Chama `root_layout.habilitar_menu(False)`
  - `login()` - Chama `root_layout.habilitar_menu(True)` após login bem-sucedido
- **VitrineScreen**: Removida linha `app.show_top_menu = True`
- **CadastroScreen**: Removida linha `app.show_top_menu = True`
- **PopupScreen**: Removido método `on_pre_enter()` completo
- **UsuarioScreen**: Removida linha `app.show_top_menu = True`
- **RelatorioScreen**: Removida linha `app.show_top_menu = True`

### menu_manager.py
- Arquivo mantido para referência, mas não é mais usado
- Métodos handler completados (_on_novo_produto, _on_novo_usuario, etc.)

## Funcionamento do Novo Menu

### Antes do Login
- Botão hambúrguer: **invisível** (opacity: 0) e **desabilitado** (disabled: True)
- Botão Sair: **invisível** (opacity: 0) e **desabilitado** (disabled: True)

### Após Login
- Botão hambúrguer: **visível** (opacity: 1) e **habilitado** (disabled: False)
- Botão Sair: **visível** (opacity: 1) e **habilitado** (disabled: False)

### Após Logout
- Volta ao estado "Antes do Login"
- Menu é automaticamente fechado se estiver aberto

### Interação com o Menu
1. Usuário clica no botão hambúrguer (☰)
2. Menu desliza da esquerda com animação suave (0.3s)
3. Overlay escuro aparece sobre o conteúdo
4. Clicar no overlay ou no botão "Fechar" fecha o menu
5. Menu desliza de volta para a esquerda

### Opções do Menu
1. **NOVO PRODUTO** - Navega para tela de cadastro de produto
2. **NOVO USUÁRIO** - Navega para tela de cadastro de usuário
3. **RELATÓRIO** - Navega para tela de relatórios
4. **LOGOMARCAR** - Abre seletor de logo (usa LogoManager)

## Detalhes Técnicos

### Overlay Touch Handling
Implementado com expressão de linha única conforme especificado:
```kv
on_touch_down: (root.menu_aberto and self.collide_point(*args[1].pos) and root.fechar_menu()) or False
```

### Animações
- Utiliza `kivy.animation.Animation` para transições suaves
- Duração: 0.3 segundos
- Easing: 'out_cubic' para movimento natural

### Estrutura do Layout
```
RootLayout (FloatLayout)
├── BoxLayout (main_content)
│   ├── BoxLayout (top_bar)
│   │   ├── Button (hambúrguer)
│   │   ├── Widget (spacer)
│   │   └── Button (sair)
│   └── BoxLayout (screen_container)
│       └── ScreenManager (adicionado programaticamente)
├── BoxLayout (side_menu) - posicionado fora da tela inicialmente
└── Widget (overlay) - overlay escuro
```

## Compatibilidade

- Todas as telas existentes continuam funcionando sem modificações
- vitrine.kv já estava preparado com botões legados ocultos
- BaseScreen continua definido em main.py via Builder.load_string()

## Testes Recomendados

1. ✓ Login - verificar que menu não aparece antes do login
2. ✓ Após login - verificar que botão hambúrguer aparece
3. ✓ Abrir menu - verificar animação e overlay
4. ✓ Navegar pelas opções do menu
5. ✓ Fechar menu clicando no overlay
6. ✓ Logout - verificar que menu desaparece
7. ✓ LOGOMARCAR - verificar integração com LogoManager

## Verificação de Migração

Todos os itens da tarefa foram concluídos:
- ✅ Parar de carregar menu.kv no main.py
- ✅ Remover herança MenuManager da classe App
- ✅ Remover propriedade show_top_menu e todas as referências
- ✅ Excluir arquivos menu.kv, base_template.kv, base_template_with_menu.kv
- ✅ Criar root_layout.kv com menu hambúrguer
- ✅ Implementar controle de visibilidade (invisível antes login, visível depois)
- ✅ Usar expressão de linha única no overlay on_touch_down
- ✅ vitrine.kv já estava preparado (botões legados ocultos)
