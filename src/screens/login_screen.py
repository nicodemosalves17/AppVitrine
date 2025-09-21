from kivy.app import App
from .base_screen import BaseScreen
from ..models.db import BancoDados

class LoginScreen(BaseScreen):
    def on_pre_enter(self):
        app = App.get_running_app()
        app.show_top_menu = False  # Oculta a topbar no login
        try:
            if hasattr(self.ids, 'logo_empresa'):
                self.ids.logo_empresa.source = app.logo_path
        except Exception:
            pass

    def login(self):
        usuario = self.ids.usuario.text.strip()
        senha = self.ids.senha.text.strip()
        perfil = BancoDados.autenticar(usuario, senha)
        app = App.get_running_app()
        if perfil:
            app.is_admin = (perfil == 'admin' or perfil == 'administrator' or perfil == 'root')
            app.show_top_menu = True  # Mostra a topbar após login
            self.manager.current = 'vitrine'
            vitrine = self.manager.get_screen('vitrine')
            vitrine.usuario_logado = usuario
            vitrine.perfil_logado = perfil
        else:
            try:
                self.ids.erro.text = "Usuário ou senha inválidos"
            except Exception:
                pass