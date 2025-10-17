from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
import os
import shutil

from db import BancoDados

from logo_manager import LogoManager

class ClickableImage(ButtonBehavior, Image):
    pass

class RootLayout(FloatLayout):
    """Root layout with screen manager container"""
    pass

# Load root_layout.kv
if os.path.exists("root_layout.kv"):
    Builder.load_file("root_layout.kv")

# Carrega os templates e telas
if os.path.exists("base_template.kv"):
    Builder.load_file("base_template.kv")

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

class LoginScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        # Hide hamburger on login screen
        try:
            root = app.root
            if hasattr(root, 'ids') and hasattr(root.ids, 'btn_hamburger'):
                root.ids.btn_hamburger.opacity = 0
                root.ids.btn_hamburger.disabled = True
        except Exception:
            pass
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
            # Show hamburger after login
            try:
                root = app.root
                if hasattr(root, 'ids') and hasattr(root.ids, 'btn_hamburger'):
                    root.ids.btn_hamburger.opacity = 1
                    root.ids.btn_hamburger.disabled = False
                    # Bind hamburger button to toggle menu
                    def toggle_menu(*args):
                        overlay = root.ids.menu_overlay
                        if overlay.opacity == 0:
                            overlay.opacity = 1
                            overlay.disabled = False
                        else:
                            overlay.opacity = 0
                            overlay.disabled = True
                    root.ids.btn_hamburger.unbind(on_release=toggle_menu)
                    root.ids.btn_hamburger.bind(on_release=toggle_menu)
            except Exception as e:
                app.print_debug(f"Error showing hamburger: {e}")
            self.manager.current = 'vitrine'
            vitrine = self.manager.get_screen('vitrine')
            vitrine.usuario_logado = usuario
            vitrine.perfil_logado = perfil
        else:
            try:
                self.ids.erro.text = "Usuário ou senha inválidos"
            except Exception:
                pass

class VitrineScreen(Screen):
    usuario_logado = ""
    perfil_logado = ""
    def on_pre_enter(self):
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

class CadastroScreen(Screen):
    imagem_path = ""
    editando = False

    def on_pre_enter(self):
        if not self.editando:
            self.limpar_campos()

    def abrir_filechooser(self):
        from kivy.uix.popup import Popup
        from kivy.uix.filechooser import FileChooserIconView
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        import os

        box = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.webp'],
            path=os.path.expanduser('~')  # Inicia na pasta do usuário
        )
        box.add_widget(filechooser)
        
        status_label = Label(
            text="Selecione uma imagem (PNG, JPG, JPEG, BMP, GIF, WEBP)", 
            size_hint_y=None, 
            height=30
        )
        box.add_widget(status_label)
        
        btn_box = BoxLayout(size_hint_y=None, height='40dp')
        btn_ok = Button(text="Selecionar")
        btn_cancel = Button(text="Cancelar")
        btn_box.add_widget(btn_ok)
        btn_box.add_widget(btn_cancel)
        box.add_widget(btn_box)
        popup = Popup(title='Escolha a imagem', content=box, size_hint=(0.9, 0.9))

        def selecionar(*args):
            if filechooser.selection:
                selected_file = filechooser.selection[0]
                
                # Validação do arquivo
                if not os.path.isfile(selected_file):
                    status_label.text = "Erro: Arquivo não encontrado"
                    return
                
                # Verifica o tamanho do arquivo (max 10MB)
                file_size = os.path.getsize(selected_file)
                if file_size > 10 * 1024 * 1024:  # 10MB
                    status_label.text = "Erro: Arquivo muito grande (máx 10MB)"
                    return
                
                # Verifica se é uma imagem válida
                valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']
                file_ext = os.path.splitext(selected_file)[1].lower()
                
                if file_ext not in valid_extensions:
                    status_label.text = "Erro: Formato de arquivo inválido"
                    return
                
                try:
                    # Tenta validar se é uma imagem real usando Pillow
                    from PIL import Image
                    with Image.open(selected_file) as img:
                        img.verify()  # Verifica se é uma imagem válida
                    
                    self.imagem_path = selected_file
                    try:
                        filename = os.path.basename(selected_file)
                        self.ids.imagem_label.text = f"✓ {filename}"
                    except Exception:
                        pass
                    popup.dismiss()
                    
                except Exception as e:
                    status_label.text = f"Erro: Arquivo de imagem inválido - {str(e)}"
                    return
            else:
                status_label.text = "Erro: Nenhum arquivo selecionado"

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

class PopupScreen(Screen):
    produto = None
    usuario_logado = ""
    perfil_logado = ""
    def on_pre_enter(self):
        pass
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

class UsuarioScreen(Screen):
    def on_pre_enter(self):
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

class RelatorioScreen(Screen):
    def on_pre_enter(self):
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

    def exportar_excel(self):
        """Exporta relatórios para arquivo Excel"""
        try:
            import pandas as pd
            from datetime import datetime
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            
            # Prepara dados do histórico
            historico = BancoDados.obter_historico()
            historico_df = pd.DataFrame(historico, columns=[
                'Código', 'Produto', 'Categoria', 'Tipo', 'Data/Hora', 'Vendedor'
            ])
            
            # Prepara dados dos produtos mais movimentados
            top_produtos = BancoDados.produtos_mais_movimentados()
            top_df = pd.DataFrame(top_produtos, columns=[
                'Produto', 'Vendido', 'Comprado'
            ])
            
            # Prepara dados do estoque
            estoque = BancoDados.relatorio_estoque()
            estoque_df = pd.DataFrame(estoque, columns=[
                'Código', 'Produto', 'Categoria', 'Total Compra', 'Total Venda', 'Estoque'
            ])
            
            # Gera nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_estoque_{timestamp}.xlsx"
            
            # Exporta para Excel com múltiplas abas
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                historico_df.to_excel(writer, sheet_name='Histórico', index=False)
                top_df.to_excel(writer, sheet_name='Top Produtos', index=False)
                estoque_df.to_excel(writer, sheet_name='Estoque', index=False)
            
            # Mostra popup de sucesso
            popup = Popup(
                title='Sucesso',
                content=Label(text=f'Relatório exportado para:\n{filename}'),
                size_hint=(None, None), 
                size=(400, 200)
            )
            popup.open()
            
        except Exception as e:
            # Mostra popup de erro
            popup = Popup(
                title='Erro',
                content=Label(text=f'Erro ao exportar Excel:\n{str(e)}'),
                size_hint=(None, None), 
                size=(400, 200)
            )
            popup.open()

    def exportar_pdf(self):
        """Exporta relatórios para arquivo PDF"""
        try:
            from fpdf import FPDF
            from datetime import datetime
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            
            # Cria PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Título
            pdf.set_font('helvetica', 'B', 16)
            pdf.cell(0, 10, 'Relatório de Estoque e Vendas', new_x='LMARGIN', new_y='NEXT', align='C')
            pdf.ln(5)
            
            # Data/hora do relatório
            pdf.set_font('helvetica', '', 10)
            pdf.cell(0, 10, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', new_x='LMARGIN', new_y='NEXT', align='C')
            pdf.ln(10)
            
            # Seção: Top Produtos
            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(0, 10, 'Produtos Mais Movimentados', new_x='LMARGIN', new_y='NEXT', align='L')
            pdf.ln(2)
            
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(80, 8, 'Produto', border=1, new_x='RIGHT', new_y='TOP', align='C')
            pdf.cell(40, 8, 'Vendido', border=1, new_x='RIGHT', new_y='TOP', align='C')
            pdf.cell(40, 8, 'Comprado', border=1, new_x='LMARGIN', new_y='NEXT', align='C')
            
            pdf.set_font('helvetica', '', 9)
            top_produtos = BancoDados.produtos_mais_movimentados()
            for produto in top_produtos[:10]:  # Top 10
                pdf.cell(80, 6, str(produto[0])[:25], border=1, new_x='RIGHT', new_y='TOP', align='L')
                pdf.cell(40, 6, str(produto[1]), border=1, new_x='RIGHT', new_y='TOP', align='C')
                pdf.cell(40, 6, str(produto[2]), border=1, new_x='LMARGIN', new_y='NEXT', align='C')
            
            pdf.ln(10)
            
            # Seção: Estoque Atual
            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(0, 10, 'Estoque Atual', new_x='LMARGIN', new_y='NEXT', align='L')
            pdf.ln(2)
            
            pdf.set_font('helvetica', 'B', 9)
            pdf.cell(25, 8, 'Código', border=1, new_x='RIGHT', new_y='TOP', align='C')
            pdf.cell(60, 8, 'Produto', border=1, new_x='RIGHT', new_y='TOP', align='C')
            pdf.cell(40, 8, 'Categoria', border=1, new_x='RIGHT', new_y='TOP', align='C')
            pdf.cell(30, 8, 'Estoque', border=1, new_x='LMARGIN', new_y='NEXT', align='C')
            
            pdf.set_font('helvetica', '', 8)
            estoque = BancoDados.relatorio_estoque()
            for item in estoque:
                pdf.cell(25, 6, str(item[0]), border=1, new_x='RIGHT', new_y='TOP', align='C')
                pdf.cell(60, 6, str(item[1])[:20], border=1, new_x='RIGHT', new_y='TOP', align='L')
                pdf.cell(40, 6, str(item[2])[:15], border=1, new_x='RIGHT', new_y='TOP', align='L')
                pdf.cell(30, 6, str(item[5]), border=1, new_x='LMARGIN', new_y='NEXT', align='C')
                
                # Quebra de página se necessário
                if pdf.get_y() > 250:
                    pdf.add_page()
                    pdf.set_font('helvetica', 'B', 9)
                    pdf.cell(25, 8, 'Código', border=1, new_x='RIGHT', new_y='TOP', align='C')
                    pdf.cell(60, 8, 'Produto', border=1, new_x='RIGHT', new_y='TOP', align='C')
                    pdf.cell(40, 8, 'Categoria', border=1, new_x='RIGHT', new_y='TOP', align='C')
                    pdf.cell(30, 8, 'Estoque', border=1, new_x='LMARGIN', new_y='NEXT', align='C')
                    pdf.set_font('helvetica', '', 8)
            
            # Salva o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_estoque_{timestamp}.pdf"
            pdf.output(filename)
            
            # Mostra popup de sucesso
            popup = Popup(
                title='Sucesso',
                content=Label(text=f'Relatório PDF exportado para:\n{filename}'),
                size_hint=(None, None), 
                size=(400, 200)
            )
            popup.open()
            
        except Exception as e:
            # Mostra popup de erro
            popup = Popup(
                title='Erro',
                content=Label(text=f'Erro ao exportar PDF:\n{str(e)}'),
                size_hint=(None, None), 
                size=(400, 200)
            )
            popup.open()

    def criar_backup(self):
        """Cria backup do banco de dados"""
        try:
            from datetime import datetime
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_produtos_{timestamp}.db"
            
            success, msg = BancoDados.backup_database(backup_filename)
            
            if success:
                popup = Popup(
                    title='Backup Criado',
                    content=Label(text=f'Backup salvo como:\n{backup_filename}'),
                    size_hint=(None, None), 
                    size=(400, 200)
                )
            else:
                popup = Popup(
                    title='Erro',
                    content=Label(text=f'Erro ao criar backup:\n{msg}'),
                    size_hint=(None, None), 
                    size=(400, 200)
                )
            popup.open()
            
        except Exception as e:
            popup = Popup(
                title='Erro',
                content=Label(text=f'Erro inesperado:\n{str(e)}'),
                size_hint=(None, None), 
                size=(400, 200)
            )
            popup.open()

class EstoqueApp(App, LogoManager):
    is_admin = BooleanProperty(False)
    logo_path = StringProperty("logo_empresa.png")  # Caminho padrão da logo

    def build(self):
        BancoDados.criar_tabela()

        # Carrega logo salva (se houver)
        try:
            if hasattr(self, 'load_logo'):
                self.load_logo(default_packaged=self.logo_path)
        except Exception:
            pass

        self.is_admin = False

        # Create ScreenManager
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(VitrineScreen(name='vitrine'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(PopupScreen(name='popup'))
        sm.add_widget(UsuarioScreen(name='usuario'))
        sm.add_widget(RelatorioScreen(name='relatorio'))
        sm.current = 'login'

        # Create RootLayout and wire ScreenManager
        root = RootLayout()
        root.screen_manager = sm
        root.ids.screen_manager_container.add_widget(sm)

        return root

    def ir_para(self, tela):
        """Navigate to a specific screen"""
        try:
            if self.root and hasattr(self.root, 'screen_manager'):
                self.root.screen_manager.current = tela
                self.print_debug(f"Navigated to: {tela}")
        except Exception as e:
            self.print_debug(f"Error navigating to {tela}: {e}")

    def print_debug(self, msg):
        """Print debug messages"""
        print(f"[DEBUG] {msg}")

    def selecionar_logo(self):
        if hasattr(self, 'open_logo_chooser'):
            self.open_logo_chooser()
        else:
            print("open_logo_chooser não disponível.")

    def logout(self):
        """Logout and return to login screen, hiding hamburger"""
        self.is_admin = False
        
        # Hide hamburger button
        try:
            if self.root and hasattr(self.root, 'ids') and hasattr(self.root.ids, 'btn_hamburger'):
                self.root.ids.btn_hamburger.opacity = 0
                self.root.ids.btn_hamburger.disabled = True
        except Exception as e:
            self.print_debug(f"Error hiding hamburger: {e}")
        
        # Navigate to login screen
        if self.root:
            try:
                if hasattr(self.root, 'screen_manager'):
                    self.root.screen_manager.current = 'login'
                else:
                    self.root.current = 'login'
            except Exception as e:
                self.print_debug(f"Error navigating to login: {e}")

if __name__ == '__main__':
    EstoqueApp().run()