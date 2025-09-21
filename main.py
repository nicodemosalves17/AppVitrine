from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import os
import shutil

from db import BancoDados

from logo_manager import LogoManager
from menu_manager import MenuManager

class ClickableImage(ButtonBehavior, Image):
    pass

# Carrega os templates e telas
if os.path.exists("base_template.kv"):
    Builder.load_file("base_template.kv")

if os.path.exists("menu.kv"):
    Builder.load_file("menu.kv")

for kv in ("login.kv", "vitrine.kv", "cadastro.kv", "popup.kv", "usuario.kv", "relatorio.kv"):
    if os.path.exists(kv):
        Builder.load_file(kv)

class BaseScreen(Screen):
    pass

Builder.load_string("""
<BaseScreen>:
    canvas.before:
        Color:
            rgba: 1, 0.647, 0, 1  # #ffa500
        Rectangle:
            pos: self.pos
            size: self.size
""")

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
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
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

class CadastroScreen(BaseScreen):
    imagem_path = ""
    editando = False

    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True
        if not self.editando:
            self.limpar_campos()

    def abrir_filechooser(self):
        from kivy.uix.popup import Popup
        from kivy.uix.filechooser import FileChooserIconView
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

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
            self.ids.descricao.text = ""
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
            self.ids.descricao.text = produto.get('descricao', '')
            self.ids.quantidade.text = str(produto['quantidade'])
            self.ids.preco.text = str(produto['preco'])
            self.ids.imagem_label.text = produto['imagem']
        except Exception:
            pass
        self.imagem_path = produto.get('imagem', '')
        self.editando = True

    def cadastrar(self):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
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
                "imagem": self.imagem_path,
                "descricao": self.ids.descricao.text.strip()
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
            self.ids.label_descricao.text = self.produto.get('descricao', '')
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
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
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
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
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

class RelatorioScreen(BaseScreen):
    def on_pre_enter(self):
        App.get_running_app().show_top_menu = True
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout

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

class EstoqueApp(App, LogoManager, MenuManager):
    is_admin = BooleanProperty(False)
    logo_path = StringProperty("logo_empresa.png")  # Caminho padrão da logo
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