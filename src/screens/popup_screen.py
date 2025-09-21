from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from .base_screen import BaseScreen
from ..models.db import BancoDados

class PopupScreen(BaseScreen):
    produto = None
    usuario_logado = ""
    perfil_logado = ""
    
    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True
        
    def carregar_produto(self, codigo):
        self.produto = BancoDados.obter_produto(codigo)
        try:
            self.ids.imagem.source = self.produto['imagem']
            self.ids.label_nome.text = self.produto['nome']
            self.ids.label_categoria.text = self.produto['categoria']
            self.ids.label_quantidade.text = f"Estoque: {self.produto['quantidade']}"
            self.ids.label_preco.text = f"R$ {self.produto['preco']:.2f}"
            self.ids.qtd_operacao.text = ""
            self.ids.btn_editar.disabled = self.perfil_logado != 'admin'
            self.ids.btn_excluir.disabled = self.perfil_logado != 'admin'
        except Exception:
            pass

    def editar(self):
        cadastro = self.manager.get_screen('cadastro')
        cadastro.preencher_campos(self.produto)
        self.manager.current = "cadastro"

    def excluir(self):
        BancoDados.excluir_produto(self.produto['codigo'])
        self.manager.current = "vitrine"

    def vender(self):
        try:
            qtd = int(self.ids.qtd_operacao.text)
            if qtd <= 0:
                raise ValueError
        except:
            popup = Popup(title='Erro',
                          content=Label(text='Informe uma quantidade válida para venda.'),
                          size_hint=(None, None), size=(350, 200))
            popup.open()
            return
        if self.produto['quantidade'] < qtd:
            popup = Popup(title='Erro',
                          content=Label(text='Estoque insuficiente.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
            return
        BancoDados.atualizar_estoque(self.produto['codigo'], self.produto['quantidade'] - qtd)
        BancoDados.registrar_operacao(self.produto, qtd, 'venda', self.usuario_logado)
        self.manager.current = "vitrine"

    def comprar(self):
        try:
            qtd = int(self.ids.qtd_operacao.text)
            if qtd <= 0:
                raise ValueError
        except:
            popup = Popup(title='Erro',
                          content=Label(text='Informe uma quantidade válida para compra.'),
                          size_hint=(None, None), size=(350, 200))
            popup.open()
            return
        BancoDados.atualizar_estoque(self.produto['codigo'], self.produto['quantidade'] + qtd)
        BancoDados.registrar_operacao(self.produto, qtd, 'compra', self.usuario_logado)
        self.manager.current = "vitrine"