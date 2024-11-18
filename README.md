# Sistema de Vendas

Este é um sistema simples de gerenciamento de vendas desenvolvido em Python, utilizando SQLite para armazenamento de dados. O sistema permite gerenciar produtos, vendas e clientes.

## Funcionalidades

- **Adicionar Produto**: Permite inserir um novo produto no sistema com seu nome, preço e quantidade em estoque.
- **Registrar Venda**: Registra vendas de produtos existentes, reduzindo automaticamente o estoque.
- **Verificar Estoque**: Permite verificar o estoque atual de um produto específico.
- **Calcular Faturamento**: Calcula o faturamento total com base nas vendas registradas.
- **Cadastrar Cliente**: Permite adicionar um novo cliente ao sistema com nome e email.
- **Sair**: Fecha a conexão com o banco de dados e encerra o sistema.

## Configuração e Execução

### Pré-requisitos

Certifique-se de ter Python instalado em sua máquina. Este sistema foi testado com Python 3.8. Além disso, é necessário que a biblioteca SQLite3 esteja disponível, o que geralmente já vem pré-instalado com a instalação padrão do Python.

### Execução

1. Salve o código do sistema em um arquivo Python, por exemplo `sistema_vendas.py`.
2. Abra o terminal ou prompt de comando.
3. Navegue até o diretório onde o arquivo foi salvo.
4. Execute o comando abaixo para iniciar o sistema:

```bash
python sistema_vendas.py
