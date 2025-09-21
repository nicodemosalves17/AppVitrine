"""
LogoManager mixin para Kivy App.

- load_logo(default_packaged): carrega logo salvo em JsonStore (user_data_dir).
- open_logo_chooser(): abre Popup com FileChooser e copia imagem para user_data_dir persistindo a escolha.
- remove_custom_logo(): remove logo salva e volta ao padrão empacotado.
"""
import os
import shutil
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform

try:
    if platform == 'android':
        from android.permissions import request_permissions, Permission
except Exception:
    Permission = None

class LogoManager:
    def load_logo(self, default_packaged='logo_empresa.png'):
        """
        Carrega logo salvo em JsonStore (em user_data_dir). Se não houver,
        usa default_packaged (nome relativo ao pacote do app).
        Deve ser chamado durante build() ou on_start() do App.
        """
        cfg_path = os.path.join(self.user_data_dir, 'config.json')
        self._store = JsonStore(cfg_path)
        if self._store.exists('logo') and os.path.exists(self._store.get('logo')['path']):
            self.logo_path = self._store.get('logo')['path']
        else:
            # fallback para logo empacotado
            if os.path.exists(default_packaged):
                self.logo_path = default_packaged
            else:
                base = os.path.dirname(os.path.abspath(__file__))
                packaged = os.path.join(base, default_packaged)
                if os.path.exists(packaged):
                    self.logo_path = packaged
                else:
                    self.logo_path = default_packaged  # keep as-is

    def ensure_permissions(self):
        """
        Pede permissão READ_EXTERNAL_STORAGE/WRITE se necessário (Android).
        """
        if Permission is None:
            return True
        try:
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            return True
        except Exception:
            return False

    def open_logo_chooser(self, title='Selecione imagem'):
        """
        Abre um Popup com FileChooser para escolher uma imagem.
        Copia para user_data_dir e persiste via JsonStore.
        """
        # tenta permissões (no Android)
        self.ensure_permissions()

        content = BoxLayout(orientation='vertical', spacing=6, padding=6)
        fc = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.webp', '*.gif', '*.bmp'])
        content.add_widget(fc)

        footer = BoxLayout(size_hint_y=None, height=40, spacing=6)
        lbl = Label(text='', size_hint_x=1)
        btn_select = Button(text='Selecionar', size_hint_x=None, width=120)
        btn_cancel = Button(text='Cancelar', size_hint_x=None, width=120)
        footer.add_widget(lbl)
        footer.add_widget(btn_select)
        footer.add_widget(btn_cancel)

        content.add_widget(footer)

        popup = Popup(title=title, content=content, size_hint=(0.95, 0.85))

        def on_select(instance):
            sel = fc.selection
            if not sel:
                lbl.text = 'Nenhum arquivo selecionado'
                return
            src = sel[0]
            try:
                dest = self._copy_logo_to_userdata(src)
                self._store.put('logo', path=dest)
                self.logo_path = dest
                # Atualiza a UI se possível (widgets que usam app.logo_path reagem automaticamente)
                try:
                    if hasattr(self, 'root') and getattr(self, 'root', None):
                        screen = None
                        try:
                            screen = self.root.get_screen('login')
                        except Exception:
                            pass
                        if screen and hasattr(screen.ids, 'logo_empresa'):
                            screen.ids.logo_empresa.source = dest
                except Exception:
                    pass
                popup.dismiss()
            except Exception as e:
                lbl.text = 'Erro ao copiar arquivo'
                print('Erro copiar logo:', e)

        btn_select.bind(on_release=on_select)
        btn_cancel.bind(on_release=lambda *a: popup.dismiss())

        popup.open()

    def _copy_logo_to_userdata(self, src_path):
        """
        Copia o arquivo src_path para user_data_dir com nome 'user_logo' + extensão.
        Retorna o caminho destino.
        """
        if not os.path.exists(src_path):
            raise FileNotFoundError(src_path)
        base, ext = os.path.splitext(src_path)
        ext = ext.lower() if ext else '.png'
        dest_name = 'user_logo' + ext
        dest = os.path.join(self.user_data_dir, dest_name)
        os.makedirs(self.user_data_dir, exist_ok=True)
        shutil.copyfile(src_path, dest)
        return dest

    def remove_custom_logo(self):
        """
        Remove logo salva (arquivos e referência em JsonStore) e volta ao logo padrão empacotado.
        """
        try:
            if self._store.exists('logo'):
                path = self._store.get('logo')['path']
                if os.path.exists(path) and os.path.commonprefix([path, self.user_data_dir]) == self.user_data_dir:
                    os.remove(path)
                self._store.delete('logo')
        except Exception:
            pass
        # fallback para padrão empacotado
        packaged = 'logo_empresa.png'
        if os.path.exists(packaged):
            self.logo_path = packaged
        # forçar update em login screen se presente
        try:
            if hasattr(self, 'root') and getattr(self, 'root', None):
                screen = None
                try:
                    screen = self.root.get_screen('login')
                except Exception:
                    pass
                if screen and hasattr(screen.ids, 'logo_empresa'):
                    screen.ids.logo_empresa.source = self.logo_path
        except Exception:
            pass