import sqlite3
from datetime import datetime

class SistemaVendas:
    def __init__(self):
        self.conn = sqlite3.connect('vendas.db')
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                preco REAL,
                estoque INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                quantidade INTEGER,
                data TEXT,
                FOREIGN KEY(produto_id) REFERENCES produtos(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def adicionar_produto(self, nome, preco, estoque):
        self.cursor.execute('INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)', (nome, preco, estoque))
        self.conn.commit()
        return "Produto adicionado com sucesso."

    def verificar_estoque(self, nome):
        self.cursor.execute('SELECT nome, estoque FROM produtos WHERE nome = ?', (nome,))
        produto = self.cursor.fetchone()
        if produto:
            resultado = f"Estoque do produto {produto[0]}: {produto[1]} unidades."
            with open("estoque.txt", "w") as file:
                file.write(resultado + "\n")
            return resultado
        else:
            return "Produto não encontrado."

    def registrar_venda(self, nome, quantidade):
        self.cursor.execute('SELECT id, preco, estoque FROM produtos WHERE nome = ?', (nome,))
        produto = self.cursor.fetchone()
        if produto and quantidade <= produto[2]:
            novo_estoque = produto[2] - quantidade
            self.cursor.execute('UPDATE produtos SET estoque = ? WHERE id = ?', (novo_estoque, produto[0]))
            self.cursor.execute('INSERT INTO vendas (produto_id, quantidade, data) VALUES (?, ?, ?)', 
                                (produto[0], quantidade, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()
            return f"Venda registrada com sucesso: {quantidade} x {nome}"
        else:
            return "Estoque insuficiente ou produto não encontrado."

    def calcular_faturamento(self):
        self.cursor.execute('SELECT SUM(p.preco * v.quantidade) FROM vendas v JOIN produtos p ON v.produto_id = p.id')
        total = self.cursor.fetchone()[0] or 0
        resultado = f"Faturamento total: R$ {total:.2f}"
        with open("faturamento.txt", "w") as file:
            file.write(resultado + "\n")
        return resultado

    def cadastrar_cliente(self, nome, email):
        self.cursor.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
        self.conn.commit()
        return "Cliente cadastrado com sucesso."

    def fechar_conexao(self):
        self.conn.close()

def converter_para_float(valor):
    try:
        return float(valor.replace(',', '.'))
    except ValueError:
        return None

def exibir_menu():
    print("\n--- Menu Sistema de Vendas ---")
    print("1. Adicionar Produto")
    print("2. Registrar Venda")
    print("3. Verificar Estoque")
    print("4. Calcular Faturamento")
    print("5. Cadastrar Cliente")
    print("6. Sair")
    return input("Escolha uma opção: ")

def main():
    sistema = SistemaVendas()
    while True:
        opcao = exibir_menu()
        if opcao == '1':
            nome = input("Nome do Produto: ")
            preco = input("Preço do Produto: ")
            preco = converter_para_float(preco)
            if preco is None:
                print("Por favor, digite um valor válido para o preço.")
                continue
            estoque = input("Quantidade em Estoque: ")
            estoque = converter_para_float(estoque)
            if estoque is None or not float(estoque).is_integer():
                print("Por favor, digite um número inteiro válido para o estoque.")
                continue
            print(sistema.adicionar_produto(nome, preco, int(estoque)))
        elif opcao == '2':
            nome = input("Nome do Produto: ")
            quantidade = input("Quantidade Vendida: ")
            quantidade = converter_para_float(quantidade)
            if quantidade is None:
                print("Por favor, digite um valor válido para a quantidade.")
                continue
            print(sistema.registrar_venda(nome, int(quantidade)))
        elif opcao == '3':
            nome = input("Nome do Produto: ")
            print(sistema.verificar_estoque(nome))
        elif opcao == '4':
            print(sistema.calcular_faturamento())
        elif opcao == '5':
            nome = input("Nome do Cliente: ")
            email = input("Email do Cliente: ")
            print(sistema.cadastrar_cliente(nome, email))
        elif opcao == '6':
            sistema.fechar_conexao()
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
