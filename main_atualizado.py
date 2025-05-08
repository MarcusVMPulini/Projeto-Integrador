#Imports ultilizados
import mysql.connector
import os

#funções utilizadas
def informacao_recebidas():
    data = str(input("Digite a data(AAAA/MM/DD): "))
    agua = float(input("Quantos litros de água você consumiu hoje? (Aprox. em litros): "))
    kwh = float(input("Quantos kWh de energia elétrica você consumiu hoje?: "))
    kg_lixo = float(input("Quantos kg de resíduos não recicláveis você gerou hoje?: "))
    lixo = float(input("Qual a porcentagem de resíduos reciclados no total (em %)?: "))
    meios_transporte = [
    "Transporte público (ônibus, metrô, trem)",
    "Bicicleta",
    "Caminhada",
    "Carro (combustível fósseis)",
    "Carro elétrico",
    "Carona compartilhada (Fósseis)"
    ]
    resposta_transporte = []


    for meio in meios_transporte:
        resposta = input(f"Você usou {meio} hoje? (S/N): ").strip().upper()    
        if resposta != 'S' and resposta != 'N':
            while resposta != 'S' and resposta != 'N':
                print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")
                resposta = input(f"Você usou {meio} hoje? (S/N): ").strip().upper() 
        resposta_transporte.append(resposta)
    
    meios_transporte_str = ",".join(resposta_transporte)

    sql = "INSERT INTO monitoramento_sustentabilidade (data_monitoramento, consumo_agua_litros, consumo_energia_kwh, residuos_nao_reciclaveis_kg, porcentagem_residuos_reciclados, meio_transporte_utilizado) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (data, agua, kwh, kg_lixo, lixo, meios_transporte_str)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Dados inseridos com sucesso!")

    return data, agua, kwh, kg_lixo, lixo, resposta_transporte

def calculo_sustentabilidade(agua, kwh, lixo, resposta_transporte):
    if resposta_transporte[0] == 'S' or resposta_transporte[1] == 'S' or resposta_transporte[2] == 'S' or resposta_transporte[4] == 'S':
        if resposta_transporte[3] == 'S' or resposta_transporte[5] == 'S':
            uso_transporte = "Média Sustentabilidade"
        else:
            uso_transporte = "Alta Sustentabilidade"
    elif resposta_transporte[5] == 'S':
        uso_transporte = "Media Sustentabilidade"
    else:
        uso_transporte = "Baixa Sustentabilidade"

    if agua < 150: 
        consumo_agua = "Alta Sustentabilidade"
    elif agua < 200:
        consumo_agua = "Moderada Sustentabilidade"
    else:
        consumo_agua = "Baixa Sustentabilidade"

    if kwh < 5: 
        consumo_energia = "Alta Sustentabilidade"
    elif kwh <= 10:
        consumo_energia = "Moderada Sustentabilidade"
    else:
        consumo_energia = "Baixa Sustentabilidade"

    if lixo > 50: 
        consumo_porcentagem_reciclados = "Alta Sustentabilidade"
    elif 20 <= lixo <= 50:
        consumo_porcentagem_reciclados = "Moderada Sustentabilidade"
    else:
        consumo_porcentagem_reciclados = "Baixa Sustentabilidade"

    return consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte

def data_especifica():
    qualdata = input("Qual a data deseja verificar?(AAAA/MM/DD) ")
    cursor.execute("Select * from monitoramento_sustentabilidade where data_monitoramento = %s", (qualdata,))
    resultado = cursor.fetchall()
    if not resultado:
            print(f"\nNenhum registro encontrado para a data {qualdata}.")
    else:
        for linha in resultado:
            resposta_transporte_db = linha[6].split(',')
            agua_db = linha[2]
            kwh_db = linha[3]
            lixo_db = linha[5]

            consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(
                agua_db, kwh_db, lixo_db, resposta_transporte_db)
            
    return qualdata, consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte

#Conexão com Banco de Dados
conexao = mysql.connector.connect(
    host="BD-ACD", 
    user="BD180225124", 
    password="Vzbbv5", 
    database="BD180225124" 
)

cursor = conexao.cursor()

if conexao.is_connected():
    print("Conexão bem-sucedida ao banco de dados!")

lobby = 10

while lobby != 0:
    print("\tMonitoriamento de Sustentabilidade")
    print("""
[ 1 ]. Verificação de Sustentabilidade
[ 2 ]. Alteração de Dados da Verificação
[ 3 ]. Apagar Dados de Verificação
[ 4 ]. Monitoriamento diário
[ 5 ]. Média de Monitoriamento
[ 6 ]. Verificar dia especifíco
[ 0 ]. Encerrar programa 
""")
    lobby = int(input())


    if lobby == 1:
        data, agua, kwh, kg_lixo, lixo, resposta_transporte = informacao_recebidas()

        consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(agua, kwh, lixo, resposta_transporte)

        print(f"""\n\n---------RESULTADOS---------\n
        Consumo de água: {consumo_agua}
        Consumo de energia: {consumo_energia}
        Geração de Resíduos Não Recicláveis: {consumo_porcentagem_reciclados}
        Uso de Transporte: {uso_transporte}
        """)

        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 2:
        print("não tem ainda")
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 3:
        print("não tem ainda")
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 4:
        print("não tem ainda")
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 5:
        print("não tem ainda")
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 6:
        qualdata, consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = data_especifica()

        print(f"""\n\n---------RESULTADOS DO DIA {qualdata}---------\n
        Consumo de água: {consumo_agua}
        Consumo de energia: {consumo_energia}
        Geração de Resíduos Não Recicláveis: {consumo_porcentagem_reciclados}
        Uso de Transporte: {uso_transporte}
        """)
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())




cursor.close()
conexao.close()