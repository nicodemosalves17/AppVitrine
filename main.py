from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
import os

# Import organized modules
from src.models.db import BancoDados
from src.managers.logo_manager import LogoManager
from src.managers.menu_manager import MenuManager

# Import screen classes
from src.screens.login_screen import LoginScreen
from src.screens.vitrine_screen import VitrineScreen
from src.screens.cadastro_screen import CadastroScreen
from src.screens.popup_screen import PopupScreen
from src.screens.usuario_screen import UsuarioScreen
from src.screens.relatorio_screen import RelatorioScreen

# Load UI templates and screens
if os.path.exists("ui/base_template.kv"):
    Builder.load_file("ui/base_template.kv")

if os.path.exists("ui/menu.kv"):
    Builder.load_file("ui/menu.kv")

for kv in ("login.kv", "vitrine.kv", "cadastro.kv", "popup.kv", "usuario.kv", "relatorio.kv"):
    kv_path = f"ui/{kv}"
    if os.path.exists(kv_path):
        Builder.load_file(kv_path)

class EstoqueApp(App, LogoManager, MenuManager):
    is_admin = BooleanProperty(False)
    logo_path = StringProperty("assets/logo_empresa.png")  # Updated path to assets
    show_top_menu = BooleanProperty(False)  # Controla visibilidade da TopMenu

    def build(self):
        BancoDados.criar_tabela()

        # Carrega logo salva (se houver)
        try:
            if hasattr(self, 'load_logo'):
                self.load_logo(default_packaged=self.logo_path)
        except Exception:
            pass

        self.is_admin = False
        self.show_top_menu = False

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(VitrineScreen(name='vitrine'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(PopupScreen(name='popup'))
        sm.add_widget(UsuarioScreen(name='usuario'))
        sm.add_widget(RelatorioScreen(name='relatorio'))
        self.root = sm

        return sm

    def selecionar_logo(self):
        if hasattr(self, 'open_logo_chooser'):
            self.open_logo_chooser()
        else:
            print("open_logo_chooser não disponível.")

    def logout(self):
        self.is_admin = False
        self.show_top_menu = False
        if self.root:
            try:
                self.root.current = 'login'
            except Exception:
                pass


if __name__ == '__main__':
    EstoqueApp().run()