data = str(input("DIgite a data: "))
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
       print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")
       resposta = input(f"Você usou {meio} hoje? (S/N): ")
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



print(f"""\n\n---------RESULTADOS---------\n
Consumo de água: {consumo_agua}
Consumo de energia: {consumo_energia}
Geração de Resíduos Não Recicláveis: {consumo_porcentagem_reciclados}
Uso de Transporte: {uso_transporte}
""")


