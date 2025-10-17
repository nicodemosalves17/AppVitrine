# Hamburger Menu Migration - Implementation Guide

## Overview
This document describes the new hamburger menu system that replaces the legacy top menu bar.

## Architecture

### Components

1. **RootLayout** (`root_layout.py` + `root_layout.kv`)
   - Main container with a FloatLayout structure
   - Contains three main areas:
     - `screen_manager_container`: Holds the ScreenManager with all app screens
     - `btn_hamburger`: The hamburger menu button (☰)
     - `menu_overlay`: The sliding menu panel with backdrop

2. **Menu State Management**
   - `menu_aberto`: Boolean property controlling menu visibility
   - `toggle_menu(abrir)`: Method to open/close the menu
   - `fechar_menu()`: Method to explicitly close the menu

3. **Screen Manager Integration**
   - ScreenManager is created in `EstoqueApp.build()`
   - Added to `screen_manager_container` in RootLayout
   - Reference stored in `root.screen_manager` for navigation

## Key Features

### Hamburger Button Behavior
- **Initially Hidden**: Opacity = 0, Disabled = True
- **After Login**: Opacity = 1, Disabled = False (enabled in LoginScreen.login())
- **After Logout**: Opacity = 0, Disabled = True (hidden in EstoqueApp.logout())
- **Position**: Top-left corner (50x50 dp)

### Menu Panel
- **Width**: 250 dp
- **Position**: Slides from left side
- **Background**: White with semi-transparent backdrop
- **Close Triggers**:
  - Clicking on backdrop
  - Selecting a menu option
  - Clicking "Sair" (logout)

### Menu Options
All options navigate to their respective screens and close the menu:

1. **Vitrine** - Always visible
2. **Novo Produto** - Admin only
3. **Novo Usuário** - Admin only  
4. **Relatório** - Always visible
5. **Trocar Logo** - Admin only (calls app.selecionar_logo())
6. **Sair** - Always visible (calls app.logout())

### Admin-Only Features
Options use opacity and disabled properties based on `app.is_admin`:
```kv
opacity: 1 if app.is_admin else 0
disabled: not app.is_admin
```

## Navigation Methods

### ir_para(tela)
```python
def ir_para(self, tela):
    """Navigate to a screen"""
    print(f"[DEBUG] Navegando para tela: {tela}")
    if self.root and self.root.screen_manager:
        self.root.screen_manager.current = tela
        print(f"[DEBUG] Tela atual: {self.root.screen_manager.current}")
```

### print_debug()
```python
def print_debug(self):
    """Debug helper"""
    print(f"[DEBUG] App root: {self.root}")
    print(f"[DEBUG] Screen manager: {self.root.screen_manager if self.root else 'N/A'}")
    print(f"[DEBUG] Current screen: {self.root.screen_manager.current if self.root and self.root.screen_manager else 'N/A'}")
    print(f"[DEBUG] Is admin: {self.is_admin}")
```

## Migration Changes

### Removed Components
- ❌ `menu.kv` - No longer loaded
- ❌ `base_template_with_menu.kv` - No longer loaded
- ❌ `MenuManager` mixin - Removed from EstoqueApp inheritance
- ❌ `show_top_menu` property - Removed from all screens
- ❌ `TopMenu` widget - No longer used
- ❌ `@BaseScreen` template inheritance - Removed from all screen KV files

### Added Components
- ✅ `root_layout.py` - RootLayout class with menu methods
- ✅ `root_layout.kv` - Hamburger menu UI definition
- ✅ `ir_para(tela)` method - Navigation helper
- ✅ `print_debug()` method - Debug helper

### Modified Components
- 🔄 `main.py` - Updated build() method, removed legacy menu code
- 🔄 All screen KV files - Now autonomous with own backgrounds
- 🔄 `LoginScreen.login()` - Shows hamburger button after successful login
- 🔄 `EstoqueApp.logout()` - Hides hamburger button and closes menu

## Screen Structure

All screens now follow this autonomous pattern:

```kv
<ScreenName>:
    canvas.before:
        Color:
            rgba: 1, 0.647, 0, 1  # Orange background
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        # Screen content here
```

## User Flow

1. **App Launch**
   - RootLayout created
   - ScreenManager added to container
   - Login screen shown
   - Hamburger button hidden

2. **Login Success**
   - Hamburger button shown (opacity = 1)
   - Navigate to Vitrine screen
   - Menu available via hamburger button

3. **Menu Interaction**
   - Click hamburger button → Menu slides in from left
   - Click menu option → Navigate + close menu
   - Click backdrop → Close menu
   - Click Sair → Logout + hide hamburger + navigate to login

4. **Logout**
   - Hamburger button hidden
   - Menu closed
   - Navigate to login screen

## Testing Checklist

- [x] RootLayout loads without errors
- [x] ScreenManager properly initialized with 6 screens
- [x] Initial screen is 'login'
- [x] Hamburger button hidden on app start
- [x] Menu toggle methods work correctly
- [x] All screen KV files load successfully
- [x] No legacy menu components referenced
- [x] Navigation methods work correctly

## File Structure

```
AppVitrine/
├── main.py                      # Updated - uses RootLayout
├── root_layout.py               # New - RootLayout class
├── root_layout.kv              # New - Hamburger menu UI
├── db.py                        # Unchanged
├── logo_manager.py              # Unchanged
├── login.kv                     # Updated - autonomous
├── vitrine.kv                   # Updated - autonomous
├── cadastro.kv                  # Updated - autonomous
├── popup.kv                     # Updated - autonomous
├── usuario.kv                   # Updated - autonomous
├── relatorio.kv                 # Updated - autonomous
├── base_template.kv             # Retained but unused
├── menu.kv                      # Not loaded (legacy)
├── base_template_with_menu.kv   # Not loaded (legacy)
└── menu_manager.py              # Not used (legacy)
```

## Notes

- The hamburger menu button (☰) is a standard Unicode character
- Menu animations (slide-in/out) are handled by KiVy's property bindings
- The backdrop uses `on_touch_down` to detect clicks and close the menu
- Admin-only options are visually hidden (opacity: 0) but still present in the widget tree
