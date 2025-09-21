```markdown
# Instruções de integração do Menu com opção de Logomarcar

O que eu entreguei:
- menu.kv: widget TopMenu (botão "Menu") que aciona um DropDown com as opções pedidas.
- menu_manager.py: mixin com handlers que realizam navegação e abrem o popup de LOGOMARCAR (que usa LogoManager quando disponível).
- base_template_with_menu.kv: exemplo de como incluir o TopMenu no topo do layout base.

Como integrar no seu projeto (passos rápidos)
1) Coloque os arquivos no diretório do seu projeto:
   - menu.kv
   - menu_manager.py
   - (opcional) base_template_with_menu.kv — substitua ou combine com seu base_template.kv

2) Misture o MenuManager na sua App (exemplo em main.py):
```python
from kivy.app import App
from logo_manager import LogoManager      # se você já estiver usando
from menu_manager import MenuManager

class EstoqueApp(App, LogoManager, MenuManager):
    def build(self):
        # carregar logo salvo
        self.load_logo()
        # Inicialmente, defina is_admin False. Após login com usuário autorizado, defina True.
        self.is_admin = False
        # load/root construction...
        root = super().build()  # substitua pela sua build actual
        return root

    # No fluxo de login, quando o usuário for autorizado:
    def on_login_success(self, user):
        # Exemplo: se user['role'] == 'admin' então:
        self.is_admin = (user.get('role') == 'admin' or user.get('is_admin', False))
        # atualiza visibilidade do menu (top widget)
        try:
            top = self.root.ids.top_menu
            # o botão já observa app.is_admin via kv; forçar refresh de layout se precisar:
            top.canvas.ask_update()
        except Exception:
            pass
```

3) Adaptar nomes de tela
- O MenuManager chama open_screen('cadastro'), open_screen('novo_usuario'), open_screen('relatorio').
- Ajuste estes nomes dentro de menu_manager.py se as suas telas tiverem ids diferentes (por exemplo: 'cadastro_produto', 'usuario_cadastrar', 'relatorios').

4) Integração com LogoManager
- Quando o usuário escolher LOGOMARCAR → Alterar imagem, o popup chama `open_logo_chooser()` do App. LogoManager implementa esse método (conforme enviei antes).
- Se você já tiver integrado LogoManager, nenhuma modificação extra é necessária.
- Se não usar LogoManager, a opção mostrará uma mensagem no log; implemente `open_logo_chooser`/`remove_custom_logo` ou integre o mixin.

5) Permissões Android
- O LogoManager solicita permissões READ/WRITE ao abrir o FileChooser. Garanta que no buildozer.spec você tenha:
    android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

6) Testes
- Compile o APK, faça login com um usuário administrador e abra o menu.
- Verifique:
  - NOVO PRODUTO e NOVO USUÁRIO abrem as telas corretas.
  - RELATÓRIO abre a tela de relatórios.
  - LOGOMARCAR abre popup com Alterar e Remover — Alterar chama o FileChooser (desktop) ou a rotina de seleção no Android (se integrado).
  - Ao remover, a logo volta ao padrão empacotado.

Observações e melhorias futuras
- Podemos transformar o menu em um menu dinâmico (carregar opções a partir de configuração/roles).
- Se preferir um menu em cascata gráfico complexo (submenus), posso implementar DropDown aninhado ou um menu lateral (NavigationDrawer).
- Se quiser que eu integre exatamente com seu main.py atual e adapte screen names automaticamente, cole aqui o conteúdo do main.py que eu modifico e retorno pronto para colar.
```