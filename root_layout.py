"""
RootLayout - Layout raiz com menu hambúrguer lateral
"""
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.animation import Animation
from kivy.metrics import dp


class RootLayout(FloatLayout):
    menu_aberto = BooleanProperty(False)
    
    def abrir_menu(self):
        """Abre o menu lateral com animação"""
        self.menu_aberto = True
        side_menu = self.ids.side_menu
        # Anima o menu deslizando para a direita
        anim = Animation(x=0, duration=0.3, t='out_cubic')
        anim.start(side_menu)
    
    def fechar_menu(self):
        """Fecha o menu lateral com animação"""
        self.menu_aberto = False
        side_menu = self.ids.side_menu
        # Anima o menu deslizando para a esquerda
        anim = Animation(x=-dp(250), duration=0.3, t='out_cubic')
        anim.start(side_menu)
        return True  # Retorna True para indicar que o touch foi consumido
    
    def menu_action(self, action):
        """Executa ação do menu"""
        from kivy.app import App
        app = App.get_running_app()
        
        # Fecha o menu primeiro
        self.fechar_menu()
        
        # Executa a ação
        if action == 'cadastro':
            try:
                cadastro = app.root.get_screen('cadastro')
                cadastro.limpar_campos()
                app.root.current = 'cadastro'
            except Exception as e:
                print(f"Erro ao navegar para cadastro: {e}")
        
        elif action == 'usuario':
            try:
                app.root.current = 'usuario'
            except Exception as e:
                print(f"Erro ao navegar para usuário: {e}")
        
        elif action == 'relatorio':
            try:
                app.root.current = 'relatorio'
            except Exception as e:
                print(f"Erro ao navegar para relatório: {e}")
        
        elif action == 'logomarcar':
            try:
                if hasattr(app, 'open_logo_chooser'):
                    app.open_logo_chooser()
                else:
                    print("open_logo_chooser não disponível.")
            except Exception as e:
                print(f"Erro ao abrir logo chooser: {e}")
    
    def habilitar_menu(self, habilitar=True):
        """Habilita ou desabilita o menu hambúrguer"""
        try:
            btn_hamburger = self.ids.btn_hamburger
            btn_sair = self.ids.btn_sair
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
                # Fecha o menu se estiver aberto
                if self.menu_aberto:
                    self.fechar_menu()
        except Exception as e:
            print(f"Erro ao habilitar/desabilitar menu: {e}")
