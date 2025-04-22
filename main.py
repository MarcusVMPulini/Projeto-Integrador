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




data = str(input("Digite a data: "))
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


cursor.close()
conexao.close()
