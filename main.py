import mysql.connector
import os

conexao = mysql.connector.connect(
    host="BD-ACD", 
    user="BD180225124", 
    password="Vzbbv5", 
    database="BD180225124" 
)

cursor = conexao.cursor()

if conexao.is_connected():
    print("Conexão bem-sucedida ao banco de dados!")




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
    consumo_agua= "Moderada Sustentabilidade"
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
elif lixo <= 50 and lixo >=20 :
    consumo_porcentagem_reciclados = "Moderada Sustentabilidade"
else:
    consumo_porcentagem_reciclados = "Baixa Sustentabilidade"


meios_transporte_str = ",".join(resposta_transporte)

sql = "INSERT INTO monitoramento_sustentabilidade (data_monitoramento, consumo_agua_litros, consumo_energia_kwh, residuos_nao_reciclaveis_kg, porcentagem_residuos_reciclados, meio_transporte_utilizado) VALUES (%s, %s, %s, %s, %s, %s)"
valores = (data, agua, kwh, kg_lixo, lixo, meios_transporte_str)
cursor.execute(sql, valores)
conexao.commit()
print("Dados inseridos com sucesso!")

print(f"""\n\n---------RESULTADOS---------\n
Consumo de água: {consumo_agua}
Consumo de energia: {consumo_energia}
Geração de Resíduos Não Recicláveis: {consumo_porcentagem_reciclados}
Uso de Transporte: {uso_transporte}
""")
pesquisa = int(input("1 - Deseja visualizar uma data especifica\n2 - Encerrar programa\n"))

if pesquisa == 1:
   qualdata = input("Qual a data deseja verificar?(AAAA/MM/DD) ")
   cursor.execute("Select * from monitoramento_sustentabilidade where data_monitoramento = %s", (qualdata,))
   resultado = cursor.fetchall()
   if not resultado:
        print(f"\nNenhum registro encontrado para a data {qualdata}.")
   else:
    for linha in resultado:
        if linha[6][0] == 'S' or linha[6][1] == 'S' or linha[6][2] == 'S' or linha[6][4] == 'S':
            if linha[6][3] == 'S' or linha[6][5] == 'S':
                uso_transporte = "Média Sustentabilidade"
            else:
                uso_transporte = "Alta Sustentabilidade"
        elif linha[6][5] == 'S':
            uso_transporte = "Media Sustentabilidade"
        else:
            uso_transporte = "Baixa Sustentabilidade"
        if linha[2] < 150: 
            consumo_agua = "Alta Sustentabilidade"
        elif linha[2] < 200:
            consumo_agua= "Moderada Sustentabilidade"
        else:
            consumo_agua = "Baixa Sustentabilidade"

        if linha[3] < 5: 
            consumo_energia = "Alta Sustentabilidade"
        elif linha[3] <= 10:
            consumo_energia = "Moderada Sustentabilidade"
        else:
            consumo_energia = "Baixa Sustentabilidade"


        if linha[5] > 50: 
            consumo_porcentagem_reciclados = "Alta Sustentabilidade"
        elif linha[5] <= 50 and lixo >=20 :
            consumo_porcentagem_reciclados = "Moderada Sustentabilidade"
        else:
            consumo_porcentagem_reciclados = "Baixa Sustentabilidade"
        
        print(f"""\n\n---------RESULTADOS DO DIA {qualdata}---------\n
        Consumo de água: {consumo_agua}
        Consumo de energia: {consumo_energia}
        Geração de Resíduos Não Recicláveis: {consumo_porcentagem_reciclados}
        Uso de Transporte: {uso_transporte}
        """)

elif pesquisa == 2:
   print("Programa encerrado")



cursor.close()
conexao.close()
