# KleberFoks_RM562225_fase2_Cap 6 - Python e além

import json
import datetime
import oracledb

# Lista para armazenar os registros de colheita
registros_colheita = []


# Função para validar entrada numérica
def entrada_float(msg):
    while True:
        try:
            valor = float(input(msg))
            if valor < 0:
                print("Digite um valor positivo.")
            else:
                return valor
        except ValueError:
            print("Valor inválido. Digite um número.")


# Função para cadastrar colheita
def cadastrar_colheita():
    print("\n--- Cadastro de Colheita ---")
    talhao = input("Informe o nome do talhão: ")
    area = entrada_float("Área colhida (em hectares): ")
    total_colhido = entrada_float("Total colhido (em toneladas): ")
    perda = entrada_float("Perda estimada (em toneladas): ")

    produtividade = total_colhido / area
    perda_percentual = (perda / (total_colhido + perda)) * 100

    registro = {
        "data": datetime.date.today().isoformat(),
        "talhao": talhao,
        "area": area,
        "colhido": total_colhido,
        "perda": perda,
        "produtividade_t_ha": round(produtividade, 2),
        "perda_percentual": round(perda_percentual, 2)
    }

    registros_colheita.append(registro)
    print("\nRegistro salvo com sucesso!")


# Função para salvar em JSON
def salvar_json():
    with open("colheita.json", "w", encoding="utf-8") as arquivo:
        json.dump(registros_colheita, arquivo, indent=4, ensure_ascii=False)
    print("Dados salvos em colheita.json")


# Função para salvar em TXT
def salvar_txt():
    with open("colheita.txt", "w", encoding="utf-8") as arquivo:
        for r in registros_colheita:
            linha = f"{r['data']} | Talhão: {r['talhao']} | Produtividade: {r['produtividade_t_ha']} t/ha | Perda: {r['perda_percentual']}%\n"
            arquivo.write(linha)
    print("Dados salvos em colheita.txt")


# Função para exportar dados para o banco Oracle
def exportar_para_oracle():
    print("\n--- Exportar dados para Oracle ---")

    try:

        # Substitua pelos dados da FIAP
        conexao = oracledb.connect(
            user="SEU_USUARIO",
            password="SUA_SENHA",
            dsn="oracle.fiap.com.br/orcl"
        )
        cursor = conexao.cursor()

        # Criar tabela se não existir
        cursor.execute("""
        BEGIN
            EXECUTE IMMEDIATE '
            CREATE TABLE colheita (
                id NUMBER GENERATED BY DEFAULT AS IDENTITY,
                data DATE,
                talhao VARCHAR2(100),
                area NUMBER,
                colhido NUMBER,
                perda NUMBER,
                produtividade_t_ha NUMBER,
                perda_percentual NUMBER
            )';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN RAISE; END IF;
        END;
        """)

        # Inserir registros
        for r in registros_colheita:
            cursor.execute("""
                INSERT INTO colheita (data, talhao, area, colhido, perda, produtividade_t_ha, perda_percentual)
                VALUES (TO_DATE(:1, 'YYYY-MM-DD'), :2, :3, :4, :5, :6, :7)
            """, (
                r["data"], r["talhao"], r["area"], r["colhido"],
                r["perda"], r["produtividade_t_ha"], r["perda_percentual"]
            ))

        conexao.commit()
        print("✅ Dados exportados com sucesso para o Oracle!")

    except oracledb.Error as e:
        print(f"❌ Erro ao exportar para o Oracle: {e}")

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass


# Menu principal
def menu():
    while True:
        print("\n=== Sistema de Controle de Perdas na Colheita ===")
        print("1. Cadastrar nova colheita")
        print("2. Salvar dados em arquivos")
        print("3. Exportar para banco de dados Oracle")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_colheita()
        elif opcao == "2":
            salvar_json()
            salvar_txt()
        elif opcao == "3":
            exportar_para_oracle()
        elif opcao == "4":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


# Execução
menu()
