from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, ObjectProperty


class RootLayout(FloatLayout):
    """Root layout with hamburger menu system"""
    menu_aberto = BooleanProperty(False)
    screen_manager = ObjectProperty(None)
    
    def toggle_menu(self, abrir=None):
        """Toggle menu open/close state"""
        if abrir is not None:
            self.menu_aberto = abrir
        else:
            self.menu_aberto = not self.menu_aberto
        print(f"Menu {'aberto' if self.menu_aberto else 'fechado'}")
    
    def fechar_menu(self):
        """Close the menu"""
        self.menu_aberto = False
        print("Menu fechado")
        return True
