# AppVitrine - Gestão de Estoque

Aplicativo Android para gestão de estoque e controle de vendas feito em Python/Kivy.

## Quick Start

```bash
pip install kivy
python main.py
```

📖 **[Documentação completa](docs/README.md)**

## Estrutura do Projeto

- `src/` - Código fonte principal (models, screens, managers)
- `ui/` - Arquivos de interface Kivy (KV files)
- `assets/` - Recursos estáticos (imagens, banco de dados)
- `docs/` - Documentação detalhada

## Build Android

Use [Buildozer](https://buildozer.readthedocs.io/en/latest/):

```bash
buildozer android debug
```