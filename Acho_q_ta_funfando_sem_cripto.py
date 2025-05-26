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
            uso_transporte = "Média"
        else:
            uso_transporte = "Alta"
    elif resposta_transporte[5] == 'S':
        uso_transporte = "Media"
    else:
        uso_transporte = "Baixa"

    if agua < 150: 
        consumo_agua = "Alta"
    elif agua < 200:
        consumo_agua = "Moderada"
    else:
        consumo_agua = "Baixa"

    if kwh < 5: 
        consumo_energia = "Alta"
    elif kwh <= 10:
        consumo_energia = "Moderada"
    else:
        consumo_energia = "Baixa"

    if lixo > 50: 
        consumo_porcentagem_reciclados = "Alta"
    elif 20 <= lixo <= 50:
        consumo_porcentagem_reciclados = "Moderada"
    else:
        consumo_porcentagem_reciclados = "Baixa"

    return consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte

def data_especifica():
    qualdata = input("Qual a data deseja verificar? (AAAA/MM/DD) ")
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (qualdata,))
    resultado = cursor.fetchall()

    if not resultado:
        print(f"\nNenhum registro encontrado para a data {qualdata}.")
    else:
        for linha in resultado:
            agua_db = linha[2]
            kwh_db = linha[3]
            lixo_db = linha[5]
            meios_transporte = linha[6]
            resposta_transporte_db = meios_transporte.split(',')

            consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(
                agua_db, kwh_db, lixo_db, resposta_transporte_db)

            print(f"""
\n---------MONITORAMENTO DIA {qualdata}---------
AGUA: {agua_db} | SUSTENTABILIDADE: {consumo_agua}
KWH: {kwh_db} | SUSTENTABILIDADE: {consumo_energia}
KG_LIXO: {lixo_db} | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}
MEIOS_TRANSPORTE: {meios_transporte} | SUSTENTABILIDADE: {uso_transporte}
""")

def apagar_todos_dados():
    data=input('Qual data voce deseja apagar(AAAA/MM/DD)?')
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (data,))
    resultado = cursor.fetchall()
    if not resultado:
            print(f"Nenhum registro encontrado para a data {data}.")
            return
    else:
        cursor.execute("DELETE FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (data,))
        conexao.commit()
        print(f"\nRegistro do dia {data} apagado com sucesso!")

def monitdiario():
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade ORDER BY data_monitoramento")
    resultados = cursor.fetchall()
    if not resultados:
        print("\nNenhum registro encontrado no banco de dados.")
        return
    for linha in resultados:
        data = linha[1]
        agua = linha[2]
        kwh = linha[3]
        kg_lixo = linha[4]
        lixo = linha[5]
        meios_transporte = linha[6]
        consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(agua,kwh,kg_lixo,lixo,meios_transporte)
        print(f'\n\n---------MONITORAMENTO DIA {data}---------')
        print(f'AGUA: {agua} | SUSTENTABILIDADE: {consumo_agua}')
        print(f'KWH: {kwh} | SUSTENTABILIDADE: {consumo_energia}')
        print(f'KG_LIXO: {kg_lixo} | SUSTENTABILIDADE: ')
        print(f'LIXO: {lixo} | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}')
        print(f'MEIOS_TRANSPORTE: {meios_transporte} | SUSTENTABILIDADE: {uso_transporte}')

def alteracao_dados():
    data=input('Qual data voce deseja alterar(AAAA/MM/DD)?')
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (data,))
    resultado = cursor.fetchall()
    if not resultado:
            print(f"Nenhum registro encontrado para a data {data}.")
            return
    else:
        for linha in resultado:
            data = linha[1]
            agua = linha[2]
            kwh = linha[3]
            kg_lixo = linha[4]
            lixo = linha[5]
            meios_transporte = linha[6]
        
        print(f"""---------DADOS DO DIA {data}---------
            Data: {data}
            Água: {agua}
            Energia: {kwh}
            Resíduos Não Recicláveis: {kg_lixo}
            Porcentagem lixo Reciclado: {lixo}
            Uso de Transporte: {meios_transporte}""")
        
        dado_alterar = int(input("""Digite qual dado deseja alterar\n
[ 1 ]. Data do monitoramento
[ 2 ]. Consumo da água
[ 3 ]. Consumo de energia
[ 4 ]. Residos não reciclaveis
[ 5 ]. Porcentagem Residos Reciclaveis
[ 6 ]. Uso de Transporte\n"""))
        
        match dado_alterar:
            case 1:
                print("Você escolheu alterar a Data do monitoramento.")
                nova_data = str(input("Digite a nova data(AAAA/MM/DD): "))
                dado = 'data_monitoramento'
            case 2:
                print("Você escolheu alterar o Consumo da água.")
                novo_dado = float(input("Quantos litros de água você consumiu hoje? (Aprox. em litros): "))
                dado = 'consumo_agua_litros'
            case 3:
                print("Você escolheu alterar o Consumo de energia.")
                novo_dado = float(input("Quantos kWh de energia elétrica você consumiu hoje?: "))
                dado = 'consumo_energia_kwh'
            case 4:
                print("Você escolheu alterar os Resíduos não recicláveis.")
                novo_dado = float(input("Quantos kg de resíduos não recicláveis você gerou hoje?: "))
                dado = 'residuos_nao_reciclaveis_kg'
            case 5:
                print("Você escolheu alterar a Porcentagem de resíduos recicláveis.")
                novo_dado = float(input("Qual a porcentagem de resíduos reciclados no total (em %)?: "))
                dado = 'porcentagem_residuos_reciclados'
            case 6:
                print("Você escolheu alterar o Uso de Transporte.")
                atualiza_meios_transporte = [
                    "Transporte público (ônibus, metrô, trem)",
                    "Bicicleta",
                    "Caminhada",
                    "Carro (combustível fósseis)",
                    "Carro elétrico",
                    "Carona compartilhada (Fósseis)"
                    ]
                new_resposta_transporte = []


                for meio in atualiza_meios_transporte:
                    resposta = input(f"Você usou {meio} hoje? (S/N): ").strip().upper()    
                    if resposta != 'S' and resposta != 'N':
                        while resposta != 'S' and resposta != 'N':
                            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")
                            resposta = input(f"Você usou {meio} hoje? (S/N): ").strip().upper() 
                    new_resposta_transporte.append(resposta)
                
                novo_dado = ",".join(resposta_transporte)
                dado = 'meio_transporte_utilizado'
            case _:
                print("Opção inválida.")
       
        cursor.execute(f"UPDATE monitoramento_sustentabilidade SET {dado} = %s WHERE data_monitoramento = %s", (novo_dado, data))
        conexao.commit()
        print(f"\nO dado {dado} do dia {data} foi alterado com Sucesso!")

        nova_data_busca = novo_dado if dado == 'data_monitoramento' else data
        cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (nova_data_busca,))
        atualizado = cursor.fetchone()

        if atualizado:
            print(f"""
---------NOVOS DADOS DO DIA {atualizado[1]}---------
Data: {atualizado[1]}
Água: {atualizado[2]} litros
Energia: {atualizado[3]} kWh
Resíduos Não Recicláveis: {atualizado[4]} kg
Porcentagem lixo Reciclado: {atualizado[5]}%
Uso de Transporte: {atualizado[6]}
""")

def media_monitoramento():
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade")
    resultados = cursor.fetchall()

    if not resultados:
        print("\nNenhum dado disponível para calcular a média.")
        return

    total_registros = len(resultados)
    soma_agua = 0
    soma_kwh = 0
    soma_lixo_kg = 0
    soma_lixo_percent = 0
    contagem_transportes = [0] * 6  

    for linha in resultados:
        soma_agua += linha[2]
        soma_kwh += linha[3]
        soma_lixo_kg += linha[4]
        soma_lixo_percent += linha[5]

        transportes = linha[6].split(',')
        for i in range(len(transportes)):
            if transportes[i].strip().upper() == 'S':
                contagem_transportes[i] += 1

    media_agua = soma_agua / total_registros
    media_kwh = soma_kwh / total_registros
    media_lixo_kg = soma_lixo_kg / total_registros
    media_lixo_percent = soma_lixo_percent / total_registros

    resposta_transporte_media = []
    for count in contagem_transportes:
        if count >= total_registros / 2:
            resposta_transporte_media.append('S')
        else:
            resposta_transporte_media.append('N')

    consumo_agua, consumo_energia, consumo_reciclados, uso_transporte = calculo_sustentabilidade(
        media_agua, media_kwh, media_lixo_percent, resposta_transporte_media
    )

    print(f"""\n\n---------MÉDIAS DO MONITORAMENTO---------\n
Média de consumo de água: {media_agua:.2f} litros | Sustentabilidade: {consumo_agua}
Média de consumo de energia: {media_kwh:.2f} kWh | Sustentabilidade: {consumo_energia}
Média de resíduos não recicláveis: {media_lixo_kg:.2f} kg
Média de reciclagem: {media_lixo_percent:.2f}% | Sustentabilidade: {consumo_reciclados}
Média de uso de transporte: Sustentabilidade: {uso_transporte}
""")

    meios_transporte = [
        "Transporte público (ônibus, metrô, trem)",
        "Bicicleta",
        "Caminhada",
        "Carro (combustível fósseis)",
        "Carro elétrico",
        "Carona compartilhada (Fósseis)"
    ]

    print("Frequência de uso dos meios de transporte:")
    for i in range(len(contagem_transportes)):
        print(f"- {meios_transporte[i]}: {contagem_transportes[i]} vezes")


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
        CONSUMO ÁGUA: {agua} | SUSTENTABILIDADE: {consumo_agua}
        KWH: {kwh} | SUSTENTABILIDADE: {consumo_energia}
        LIXO: {lixo} | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}
        MEIOS_TRANSPORTE: {resposta_transporte} | SUSTENTABILIDADE: {uso_transporte}
        """)

        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 2:
        alteracao_dados()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 3:
        apagar_todos_dados()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 4:
        monitdiario()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 5:
        media_monitoramento
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())

    elif lobby == 6:
        
        data_especifica()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        lobby = int(input())




cursor.close()
conexao.close()