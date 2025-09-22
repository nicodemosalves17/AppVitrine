"""
MenuManager mixin — versão que injeta o menu na camada overlay do Screen atual.
- Garante que o menu fique acima de quaisquer widgets da tela (produtos, imagens, etc.).
- O menu é composto por um backdrop (captura cliques e fecha) e um BoxLayout com botões.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class MenuManager:
    def open_main_menu(self, widget):
        """
        Abre o menu principal anexado ao overlay_layer do screen atual.
        widget: o botão que solicitou o menu (usado para posicionar perto dele).
        """
        # tenta obter o screen atual
        try:
            if not hasattr(self, 'root') or not self.root:
                return
            # root é ScreenManager — pega screen atual
            current = None
            try:
                current = self.root.get_screen(self.root.current)
            except Exception:
                # fallback: talvez root seja a própria Screen, então use root
                current = self.root
            if current is None:
                return
            overlay = current.ids.get('overlay_layer') if hasattr(current, 'ids') else None
            if overlay is None:
                # fallback simples: nada a fazer
                return
        except Exception:
            return

        # cria backdrop (captura toques e fecha menu) - fundo semi-transparente
        backdrop = Button(size_hint=(1, 1), pos=(0, 0), background_color=(0, 0, 0, 0.3))
        # backdrop com efeito visual de fundo escuro para destacar o menu

        # cria caixa do menu
        menu_items = [
            ("NOVO PRODUTO", self._on_novo_produto),
            ("NOVO USUÁRIO", self._on_novo_usuario),
            ("RELATÓRIO", self._on_relatorio),
            ("LOGOMARCAR", self._on_logomarcar),
        ]
        menu_height = dp((len(menu_items) + 1) * 42)  # +1 para botão cancelar
        menu_width = dp(160)

        menu_box = BoxLayout(orientation='vertical', size_hint=(None, None),
                             width=menu_width, height=menu_height, spacing=6, padding=6)

        # opcões
        for label_text, handler in menu_items:
            b = Button(text=label_text, size_hint_y=None, height=dp(40))
            def _make(h):
                def _handle(instance):
                    _remove()
                    try:
                        h()
                    except Exception as e:
                        print("Erro ao executar ação do menu:", e)
                return _handle
            b.bind(on_release=_make(handler))
            menu_box.add_widget(b)

        # cancelar
        btn_cancel = Button(text="Cancelar", size_hint_y=None, height=dp(36))
        btn_cancel.bind(on_release=lambda *a: _remove())
        menu_box.add_widget(btn_cancel)

        # desenho de fundo melhorado - adiciona canvas ao menu_box
        with menu_box.canvas.before:
            Color(1, 1, 1, 0.95)  # fundo branco quase opaco
            bg = RoundedRectangle(size=(menu_box.width, menu_box.height), pos=menu_box.pos, radius=[dp(8)])
        # borda sutil para destacar o menu
        with menu_box.canvas.after:
            Color(0.8, 0.8, 0.8, 0.8)  # borda cinza claro
            from kivy.graphics import Line
            border = Line(rounded_rectangle=[menu_box.x, menu_box.y, menu_box.width, menu_box.height, dp(8)], width=1)
        # atualiza bg e border com mudanças de pos/size
        def _update_bg(*a):
            try:
                bg.size = (menu_box.width, menu_box.height)
                bg.pos = menu_box.pos
                border.rounded_rectangle = [menu_box.x, menu_box.y, menu_box.width, menu_box.height, dp(8)]
            except Exception:
                pass
        menu_box.bind(pos=_update_bg, size=_update_bg)

        # função que remove menu e backdrop do overlay
        def _remove(*a):
            try:
                if menu_box.parent:
                    overlay.remove_widget(menu_box)
            except Exception:
                pass
            try:
                if backdrop.parent:
                    overlay.remove_widget(backdrop)
            except Exception:
                pass

        # add backdrop primeiro (fica abaixo), depois menu_box (fica acima)
        overlay.add_widget(backdrop)
        overlay.add_widget(menu_box)

        # posiciona menu_box próximo ao widget (convertendo coords entre janelas)
        try:
            # posição do botão no sistema de coordenadas da janela
            wx, wy = widget.to_window(widget.x, widget.y)
            top_y = wy + widget.height
            # converte coordenada janela -> coordenada local do overlay
            local_x, local_y = overlay.to_widget(wx, top_y)
            # queremos o menu dropdown abaixo do botão hambúrguer
            menu_x = local_x
            menu_y = local_y - menu_box.height - dp(8)
            
            # garante que o menu fique dentro da tela
            if menu_x + menu_box.width > overlay.width:
                menu_x = max(dp(6), overlay.width - menu_box.width - dp(6))
            if menu_y < 0:
                # se não cabe abaixo, coloca acima do botão
                _, top_y = widget.to_window(widget.x, widget.y + widget.height)
                _, local_y = overlay.to_widget(0, top_y)
                menu_y = local_y + dp(8)
                # se ainda não couber, força no topo da tela
                if menu_y + menu_box.height > overlay.height:
                    menu_y = dp(6)
            menu_box.pos = (menu_x, menu_y)
        except Exception:
            # fallback: canto superior esquerdo com margin, garantindo visibilidade
            menu_box.pos = (dp(8), overlay.height - menu_box.height - dp(8))

        # fecha o menu se o usuário clicar no backdrop
        backdrop.bind(on_release=lambda *a: _remove())

    def _on_novo_produto(self):
        """Navega para a tela de cadastro de produto"""
        try:
            if hasattr(self, 'root') and self.root:
                self.root.current = 'cadastro'
        except Exception as e:
            print("Erro ao abrir tela de cadastro:", e)

    def _on_novo_usuario(self):
        """Navega para a tela de cadastro de usuário"""
        try:
            if hasattr(self, 'root') and self.root:
                self.root.current = 'usuario'
        except Exception as e:
            print("Erro ao abrir tela de usuário:", e)

    def _on_relatorio(self):
        """Navega para a tela de relatórios"""
        try:
            if hasattr(self, 'root') and self.root:
                self.root.current = 'relatorio'
        except Exception as e:
            print("Erro ao abrir tela de relatório:", e)

    def _on_logomarcar(self):
        """Abre opções para alterar ou remover logo"""
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.button import Button
            from kivy.uix.label import Label

            content = BoxLayout(orientation='vertical', spacing=10)
            content.add_widget(Label(text='Escolha uma opção:', size_hint_y=None, height=30))
            
            btn_alterar = Button(text='Alterar Logo', size_hint_y=None, height=40)
            btn_remover = Button(text='Remover Logo', size_hint_y=None, height=40)
            btn_cancelar = Button(text='Cancelar', size_hint_y=None, height=40)
            
            content.add_widget(btn_alterar)
            content.add_widget(btn_remover)
            content.add_widget(btn_cancelar)

            popup = Popup(title='Logomarcar', content=content, size_hint=(0.6, 0.4))

            def alterar_logo(*args):
                popup.dismiss()
                if hasattr(self, 'open_logo_chooser'):
                    self.open_logo_chooser()
                else:
                    print("Funcionalidade de alteração de logo não disponível")

            def remover_logo(*args):
                popup.dismiss()
                if hasattr(self, 'remove_custom_logo'):
                    self.remove_custom_logo()
                else:
                    print("Funcionalidade de remoção de logo não disponível")

            btn_alterar.bind(on_release=alterar_logo)
            btn_remover.bind(on_release=remover_logo)
            btn_cancelar.bind(on_release=lambda x: popup.dismiss())

            popup.open()
        except Exception as e:
            print("Erro ao abrir popup de logomarcar:", e)