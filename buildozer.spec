[app]
# Nome do teu app
title = appvitrine
package.name = appvitrine

# Script principal
entrypoint = main.py

# Versão
version = 0.1

# Diretório fonte e extensões que devem ser incluídas
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,txt

# Dependências Python
requirements = python3,kivy,pillow,pandas,fpdf

# Permissões Android necessárias para salvar/ler PDF e arquivos
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# API / Min API
android.api = 33
android.minapi = 21

# NDK (versão estável compatível)
android.ndk = 25b

# Força empacotar tudo (ajuda com alguns módulos como kivymd)
# (Opcional: se tiveres problemas com kivymd, podes copiar a pasta kivymd para o teu projeto e não depender da instalação externa)
# garden_requirements =

# Ativa a coleta de logs mais verbosa se precisar
# log_level = 2

[buildozer]
# nível de log
log_level = 2
