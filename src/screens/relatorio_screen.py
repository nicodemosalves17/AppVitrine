from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from .base_screen import BaseScreen
from ..models.db import BancoDados

class RelatorioScreen(BaseScreen):
    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True
        
        # ---------- HISTÓRICO ----------
        try:
            self.ids.historico_grid.clear_widgets()
        except Exception:
            pass
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        for title, width in zip(["CÓDIGO", "PRODUTO", "CATEGORIA", "DATA", "VENDEDOR"], [80, 160, 120, 140, 120]):
            header.add_widget(Label(text=f"[b]{title}[/b]", markup=True, size_hint_x=None, width=width))
        try:
            self.ids.historico_grid.add_widget(header)
        except Exception:
            pass

        historico = BancoDados.obter_historico()
        for h in historico:
            line = BoxLayout(orientation='horizontal', size_hint_y=None, height=25)
            for text, width in zip([h[0], h[1], h[2], h[4], h[5]], [80, 160, 120, 140, 120]):
                line.add_widget(Label(text=str(text), size_hint_x=None, width=width, shorten=True, max_lines=1))
            try:
                self.ids.historico_grid.add_widget(line)
            except Exception:
                pass

        # ---------- TOP PRODUTOS ----------
        try:
            self.ids.top_grid.clear_widgets()
        except Exception:
            pass
        top_header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        for title, width in zip(["PRODUTO", "VENDIDO", "COMPRADO"], [200, 100, 100]):
            top_header.add_widget(Label(text=f"[b]{title}[/b]", markup=True, size_hint_x=None, width=width))
        try:
            self.ids.top_grid.add_widget(top_header)
        except Exception:
            pass

        top = BancoDados.produtos_mais_movimentados()
        for t in top:
            line = BoxLayout(orientation='horizontal', size_hint_y=None, height=25)
            for text, width in zip([t[0], t[1], t[2]], [200, 100, 100]):
                line.add_widget(Label(text=str(text), size_hint_x=None, width=width, shorten=True, max_lines=1))
            try:
                self.ids.top_grid.add_widget(line)
            except Exception:
                pass

        # ---------- ESTOQUE ----------
        try:
            self.ids.estoque_grid.clear_widgets()
        except Exception:
            pass
        estoque_header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        for title, width in zip(["CÓDIGO", "PRODUTO", "CATEGORIA", "COMPRA", "VENDA", "ESTOQUE"], [80, 160, 120, 90, 90, 90]):
            estoque_header.add_widget(Label(text=f"[b]{title}[/b]", markup=True, size_hint_x=None, width=width))
        try:
            self.ids.estoque_grid.add_widget(estoque_header)
        except Exception:
            pass

        estoque_dados = BancoDados.relatorio_estoque()
        for item in estoque_dados:
            line = BoxLayout(orientation='horizontal', size_hint_y=None, height=25)
            for text, width in zip(item, [80, 160, 120, 90, 90, 90]):
                line.add_widget(Label(text=str(text), size_hint_x=None, width=width, shorten=True, max_lines=1))
            try:
                self.ids.estoque_grid.add_widget(line)
            except Exception:
                pass