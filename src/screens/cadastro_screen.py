from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from .base_screen import BaseScreen
from ..models.db import BancoDados

class CadastroScreen(BaseScreen):
    imagem_path = ""
    editando = False

    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True
        if not self.editando:
            self.limpar_campos()

    def abrir_filechooser(self):
        box = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif'])
        box.add_widget(filechooser)
        btn_box = BoxLayout(size_hint_y=None, height='40dp')
        btn_ok = Button(text="Selecionar")
        btn_cancel = Button(text="Cancelar")
        btn_box.add_widget(btn_ok)
        btn_box.add_widget(btn_cancel)
        box.add_widget(btn_box)
        popup = Popup(title='Escolha a imagem', content=box, size_hint=(0.9, 0.9))

        def selecionar(*args):
            if filechooser.selection:
                self.imagem_path = filechooser.selection[0]
                try:
                    self.ids.imagem_label.text = self.imagem_path
                except Exception:
                    pass
            popup.dismiss()

        def cancelar(*args):
            popup.dismiss()

        btn_ok.bind(on_release=selecionar)
        btn_cancel.bind(on_release=cancelar)
        popup.open()

    def limpar_campos(self):
        try:
            self.ids.codigo.text = ""
            self.ids.nome.text = ""
            self.ids.categoria.text = ""
            self.ids.quantidade.text = ""
            self.ids.preco.text = ""
            self.ids.imagem_label.text = "Nenhuma imagem selecionada"
        except Exception:
            pass
        self.imagem_path = ""
        self.editando = False

    def preencher_campos(self, produto):
        try:
            self.ids.codigo.text = produto['codigo']
            self.ids.nome.text = produto['nome']
            self.ids.categoria.text = produto['categoria']
            self.ids.quantidade.text = str(produto['quantidade'])
            self.ids.preco.text = str(produto['preco'])
            self.ids.imagem_label.text = produto['imagem']
        except Exception:
            pass
        self.imagem_path = produto.get('imagem', '')
        self.editando = True

    def cadastrar(self):
        if not self.imagem_path:
            popup = Popup(title='Erro',
                          content=Label(text='A imagem é obrigatória.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
            return
        if not all([self.ids.codigo.text.strip(), self.ids.nome.text.strip(),
                    self.ids.categoria.text.strip(), self.ids.quantidade.text.strip(),
                    self.ids.preco.text.strip()]):
            popup = Popup(title='Erro',
                          content=Label(text='Preencha todos os campos.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
            return
        try:
            dados = {
                "codigo": self.ids.codigo.text.strip(),
                "nome": self.ids.nome.text.strip(),
                "categoria": self.ids.categoria.text.strip(),
                "quantidade": int(self.ids.quantidade.text),
                "preco": float(self.ids.preco.text),
                "imagem": self.imagem_path
            }
        except ValueError:
            popup = Popup(title='Erro',
                          content=Label(text='Quantidade deve ser número inteiro e preço deve ser número decimal.'),
                          size_hint=(None, None), size=(350, 200))
            popup.open()
            return
        BancoDados.cadastrar_produto(dados)
        self.limpar_campos()
        self.manager.current = "vitrine"