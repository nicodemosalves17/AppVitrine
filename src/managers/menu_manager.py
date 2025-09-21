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

        # cria backdrop (captura toques e fecha menu)
        backdrop = Button(size_hint=(1, 1), pos=(0, 0), background_color=(0, 0, 0, 0.0))
        # make backdrop slightly semitransparente if you want masking effect:
        # backdrop.background_color = (0,0,0,0.15)

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

        # desenho simples de fundo (opcional) - adiciona canvas ao menu_box
        with menu_box.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            bg = RoundedRectangle(size=(menu_box.width, menu_box.height), pos=menu_box.pos, radius=[6])
        # atualiza bg com mudanças de pos/size
        def _update_bg(*a):
            try:
                bg.size = (menu_box.width, menu_box.height)
                bg.pos = menu_box.pos
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
            # queremos o canto superior esquerdo do menu alinhado ao topo do widget
            menu_x = local_x
            menu_y = local_y - menu_box.height - dp(4)
            # corrige limites para não sair da tela/overlay
            if menu_x + menu_box.width > overlay.width:
                menu_x = max(dp(6), overlay.width - menu_box.width - dp(6))
            if menu_y < 0:
                menu_y = dp(6)
            menu_box.pos = (menu_x, menu_y)
        except Exception:
            # fallback: canto superior esquerdo com margin
            menu_box.pos = (dp(8), overlay.height - menu_box.height - dp(8))

        # fecha o menu se o usuário clicar no backdrop
        backdrop.bind(on_release=lambda *a: _remove())