from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from .base_screen import BaseScreen
from ..models.db import BancoDados
from ..components import ClickableImage

class VitrineScreen(BaseScreen):
    usuario_logado = ""
    perfil_logado = ""
    
    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True  # Garante topbar visível
        try:
            self.ids.produtos_box.clear_widgets()
        except Exception:
            pass
        produtos = BancoDados.obter_todos_produtos()
        try:
            self.ids.btn_cadastro.disabled = (self.perfil_logado != 'admin')
            self.ids.btn_cad_usuario.disabled = (self.perfil_logado != 'admin')
        except Exception:
            pass
        for produto in produtos:
            self.add_produto_card(produto)

    def add_produto_card(self, produto):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=180, padding=5)
        img = ClickableImage(source=produto.get('imagem', ''), size_hint_y=1)
        img.bind(on_release=lambda x: self.abrir_popup(produto['codigo']))
        box.add_widget(img)
        box.add_widget(
            Label(
                text=produto.get('nome', ''),
                font_size=14,
                size_hint_y=None,
                height=30
            )
        )
        try:
            self.ids.produtos_box.add_widget(box)
        except Exception:
            pass

    def abrir_popup(self, codigo):
        popup = self.manager.get_screen('popup')
        popup.usuario_logado = self.usuario_logado
        popup.perfil_logado = self.perfil_logado
        popup.carregar_produto(codigo)
        self.manager.current = 'popup'

    def novo_cadastro(self):
        cadastro = self.manager.get_screen('cadastro')
        cadastro.limpar_campos()
        self.manager.current = "cadastro"