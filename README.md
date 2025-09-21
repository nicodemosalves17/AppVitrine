# App de Gestão de Estoque e Controle de Vendas

Aplicativo Android feito em Python/Kivy para pequenas empresas.

## Funcionalidades

- Cadastro, edição e exclusão de produtos
- Registro de vendas e compras com atualização automática do estoque
- Banco de dados local SQLite
- Imagem **anexada** obrigatoriamente para cada produto

## Como rodar

1. Instale Python 3 e Kivy (`pip install kivy`).
2. Execute: `python main.py`
3. Para gerar APK, use [Buildozer](https://buildozer.readthedocs.io/en/latest/).

## Observações

- Use o botão "Selecionar Imagem" para anexar uma imagem do seu computador.
- O caminho da imagem ficará salvo no banco de dados e será exibido na vitrine e no popup.
- Para Android, use [plyer](https://github.com/kivy/plyer) para acesso à galeria/câmera.

## Estrutura do banco de dados

- **Código**
- **Nome**
- **Categoria**
- **Descrição** (opcional - descrição curta do produto)
- **Quantidade**
- **Preço**
- **Imagem** (obrigatória - caminho local)