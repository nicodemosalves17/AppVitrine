from kivy.app import App
from .base_screen import BaseScreen
from ..models.db import BancoDados

class UsuarioScreen(BaseScreen):
    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True
        self.limpar_campos()

    def limpar_campos(self):
        try:
            self.ids.usuario.text = ""
            self.ids.senha.text = ""
            self.ids.perfil.text = "usuario"
            self.ids.msg.text = ""
        except Exception:
            pass

    def cadastrar_usuario(self):
        usuario = self.ids.usuario.text.strip()
        senha = self.ids.senha.text.strip()
        perfil = self.ids.perfil.text
        if not usuario or not senha:
            self.ids.msg.text = "[color=ff0000]Usuário e senha obrigatórios![/color]"
            return
        ok, msg = BancoDados.cadastrar_usuario(usuario, senha, perfil)
        if ok:
            self.ids.msg.text = "[color=00aa00]Usuário cadastrado com sucesso![/color]"
            self.limpar_campos()
        else:
            self.ids.msg.text = f"[color=ff0000]{msg}[/color]"