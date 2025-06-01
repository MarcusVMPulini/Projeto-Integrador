import mysql.connector
from sympy import Matrix

# ========== MÓDULO DE CRIPTOGRAFIA ==========
# ----------- CRIPTOGRAFAR TEXTO -------------
class CriptografiaHill:
    def __init__(self):
        self.key_matrix = Matrix([[3, 3], [2, 5]])
        self.modulo = 26
    
    def text_to_numbers(self, text):
        return [ord(c) - ord('A') for c in text.upper() if c.isalpha()]
    
    def numbers_to_text(self, numbers):
        return ''.join(chr(int(n % 26) + ord('A')) for n in numbers)
    
    def criptografar_texto(self, texto):
        texto = str(texto).upper().replace(" ", "").replace(".", "").replace(",", "").replace("/", "").replace("-", "")
        texto_limpo = ''.join(c for c in texto if c.isalnum())
        
        if len(texto_limpo) % 2 != 0:
            texto_limpo += 'X' 
        
        numeros = self.text_to_numbers(texto_limpo)
        if not numeros:
            return str(texto)
        
        if len(numeros) % 2 != 0:
            numeros.append(0)
        
        resultado = []
        for i in range(0, len(numeros), 2):
            bloco = Matrix([numeros[i], numeros[i + 1]])
            cifrado = self.key_matrix * bloco % self.modulo
            resultado.extend(cifrado)
        
        return self.numbers_to_text(resultado)
    
    def descriptografar_texto(self, texto_cifrado):
        if not isinstance(texto_cifrado, str):
            return texto_cifrado

        numeros = self.text_to_numbers(texto_cifrado)
        if not numeros:
            return texto_cifrado

        resultado = []
        inverse_key = self.key_matrix.inv_mod(self.modulo)

        for i in range(0, len(numeros), 2):
            bloco = Matrix([numeros[i], numeros[i + 1]])
            decifrado = inverse_key * bloco % self.modulo
            resultado.extend(decifrado)

        texto = self.numbers_to_text(resultado)
        texto = texto.rstrip('X')
        return texto

# ----------- CRIPTOGRAFAR NÚMERO -------------

class CriptografiaNumero:
    def __init__(self, deslocamento=3):
        self.deslocamento = deslocamento
    
    def criptografar_numero(self, numero):
        texto_num = str(numero)
        return ''.join(chr(ord(c) + self.deslocamento) for c in texto_num)
    
    def descriptografar_numero(self, texto_cifrado):
        return ''.join(chr(ord(c) - self.deslocamento) for c in texto_cifrado)
    
def formatar_data(data):
    """Formata a data no formato AAAA/MM/DD"""
    return f"{data[:4]}/{data[4:6]}/{data[6:8]}"

# Puxando as funções de criptografia
cripto_texto = CriptografiaHill()
cripto_numero = CriptografiaNumero()

# ========== FUNÇÕES DO SISTEMA ==========
# ------- Função para inserir dados ----------
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
        while resposta not in ['S', 'N']:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")
            resposta = input(f"Você usou {meio} hoje? (S/N): ").strip().upper()
        resposta_transporte.append(resposta)
    
    resposta_transporte_str = ''.join(resposta_transporte)

    data_cripto = cripto_texto.criptografar_texto(data)
    agua_cripto = cripto_numero.criptografar_numero(agua)
    kwh_cripto = cripto_numero.criptografar_numero(kwh)
    kg_lixo_cripto = cripto_numero.criptografar_numero(kg_lixo)
    lixo_cripto = cripto_numero.criptografar_numero(lixo)
    transporte_cripto = cripto_texto.criptografar_texto(resposta_transporte_str)
    
    sql = "INSERT INTO monitoramento_sustentabilidade (data_monitoramento, consumo_agua_litros, consumo_energia_kwh, residuos_nao_reciclaveis_kg, porcentagem_residuos_reciclados, meio_transporte_utilizado) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (data_cripto, agua_cripto, kwh_cripto, kg_lixo_cripto, lixo_cripto, transporte_cripto)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Dados inseridos com sucesso!")
    return data, agua, kwh, kg_lixo, lixo, resposta_transporte


# ------- Função para calcular dados ----------
def calculo_sustentabilidade(agua, kwh, lixo, resposta_transporte):
    if len(resposta_transporte) == 6:
        if resposta_transporte[0] == 'S' or resposta_transporte[1] == 'S' or resposta_transporte[2] == 'S' or resposta_transporte[4] == 'S':
            if resposta_transporte[3] == 'S' or resposta_transporte[5] == 'S':
                uso_transporte = "Média"
            else:
                uso_transporte = "Alta"
        elif resposta_transporte[5] == 'S':
            uso_transporte = "Média"
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
    else:
        consumo_agua = consumo_energia = consumo_porcentagem_reciclados = uso_transporte = "Indefinido"
    
    return consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte

def descriptografar_registro(linha):
    id_reg = linha[0]
    data_desc = cripto_texto.descriptografar_texto(linha[1])
    data_desc_formatada = formatar_data(data_desc)
    agua_desc = float(cripto_numero.descriptografar_numero(linha[2]))
    kwh_desc = float(cripto_numero.descriptografar_numero(linha[3]))
    kg_lixo_desc = float(cripto_numero.descriptografar_numero(linha[4]))
    lixo_desc = float(cripto_numero.descriptografar_numero(linha[5]))
    transporte_desc = cripto_texto.descriptografar_texto(linha[6])
    
    return id_reg, data_desc_formatada, agua_desc, kwh_desc, kg_lixo_desc, lixo_desc, transporte_desc

# ------- Função para verificar data especifica ----------

def data_especifica():
    qualdata = input("Qual a data deseja verificar? (AAAA/MM/DD) ")
    qualdata_cripto = cripto_texto.criptografar_texto(qualdata.replace("/", ""))
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (qualdata_cripto,))
    resultado = cursor.fetchall()
    
    if not resultado:
        print(f"\nNenhum registro encontrado para a data {qualdata}.")
    else:
        for linha in resultado:
            id_reg, data_desc, agua_desc, kwh_desc, kg_lixo_desc, lixo_desc, transporte_desc = descriptografar_registro(linha)
            resposta_transporte_db = list(transporte_desc)
            consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(
                agua_desc, kwh_desc, lixo_desc, resposta_transporte_db)
            print(f"""
\n---------MONITORAMENTO DIA {data_desc}---------
AGUA: {agua_desc} | SUSTENTABILIDADE: {consumo_agua}
KWH: {kwh_desc} | SUSTENTABILIDADE: {consumo_energia}
KG_LIXO: {kg_lixo_desc} | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}
MEIOS_TRANSPORTE: {transporte_desc} | SUSTENTABILIDADE: {uso_transporte}
""")
            
# ------- Função para apagar dados ----------

def apagar_todos_dados():
    data = input('Qual data você deseja apagar(AAAA/MM/DD)? ')
    data_cripto = cripto_texto.criptografar_texto(data.replace("/", ""))
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (data_cripto,))
    resultado = cursor.fetchall()
    
    if not resultado:
        print(f"Nenhum registro encontrado para a data {data}.")
        return
    else:
        cursor.execute("DELETE FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (data_cripto,))
        conexao.commit()
        print(f"\nRegistro do dia {data} apagado com sucesso!")


# ------- Função para monitoramento diário ----------
def monitdiario():
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade ORDER BY data_monitoramento")
    resultados = cursor.fetchall()
    
    if not resultados:
        print("\nNenhum registro encontrado no banco de dados.")
        return
    
    for linha in resultados:
        id_reg, data_desc, agua_desc, kwh_desc, kg_lixo_desc, lixo_desc, transporte_desc = descriptografar_registro(linha)
        resposta_transporte_db = list(transporte_desc)
        consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(
            agua_desc, kwh_desc, lixo_desc, resposta_transporte_db)
        
        print(f'\n\n---------MONITORAMENTO DIA {data_desc}---------')
        print(f'AGUA: {agua_desc} | SUSTENTABILIDADE: {consumo_agua}')
        print(f'KWH: {kwh_desc} | SUSTENTABILIDADE: {consumo_energia}')
        print(f'KG_LIXO: {kg_lixo_desc} | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}')
        print(f'LIXO: {lixo_desc}% | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}')
        print(f'MEIOS_TRANSPORTE: {transporte_desc} | SUSTENTABILIDADE: {uso_transporte}')


# ------- Função para alterar dados ----------
def alteracao_dados():
    data = input('Qual data você deseja alterar(AAAA/MM/DD)? ')
    data_cripto = cripto_texto.criptografar_texto(data.replace("/", ""))
    cursor.execute("SELECT * FROM monitoramento_sustentabilidade WHERE data_monitoramento = %s", (data_cripto,))
    resultado = cursor.fetchall()
    
    if not resultado:
        print(f"Nenhum registro encontrado para a data {data}.")
        return
    else:
        for linha in resultado:
            id_reg, data_desc, agua_desc, kwh_desc, kg_lixo_desc, lixo_desc, transporte_desc = descriptografar_registro(linha)
        
        print(f"""---------DADOS DO DIA {data_desc}---------
Data: {data_desc}
Água: {agua_desc}
Energia: {kwh_desc}
Resíduos Não Recicláveis: {kg_lixo_desc}
Porcentagem lixo Reciclado: {lixo_desc}
Uso de Transporte: {transporte_desc}""")
        
        dado_alterar = int(input("""Digite qual dado deseja alterar\n
[ 1 ]. Data do monitoramento
[ 2 ]. Consumo da água
[ 3 ]. Consumo de energia
[ 4 ]. Resíduos não recicláveis
[ 5 ]. Porcentagem Resíduos Recicláveis
[ 6 ]. Uso de Transporte\n"""))
        
        match dado_alterar:
            case 1:
                print("Você escolheu alterar a Data do monitoramento.")
                nova_data = str(input("Digite a nova data(AAAA/MM/DD): "))
                novo_dado_cripto = cripto_texto.criptografar_texto(nova_data)
                dado = 'data_monitoramento'
            case 2:
                print("Você escolheu alterar o Consumo da água.")
                novo_dado = float(input("Quantos litros de água você consumiu hoje? (Aprox. em litros): "))
                novo_dado_cripto = cripto_numero.criptografar_numero(novo_dado)
                dado = 'consumo_agua_litros'
            case 3:
                print("Você escolheu alterar o Consumo de energia.")
                novo_dado = float(input("Quantos kWh de energia elétrica você consumiu hoje?: "))
                novo_dado_cripto = cripto_numero.criptografar_numero(novo_dado)
                dado = 'consumo_energia_kwh'
            case 4:
                print("Você escolheu alterar os Resíduos não recicláveis.")
                novo_dado = float(input("Quantos kg de resíduos não recicláveis você gerou hoje?: "))
                novo_dado_cripto = cripto_numero.criptografar_numero(novo_dado)
                dado = 'residuos_nao_reciclaveis_kg'
            case 5:
                print("Você escolheu alterar a Porcentagem de resíduos recicláveis.")
                novo_dado = float(input("Qual a porcentagem de resíduos reciclados no total (em %)?: "))
                novo_dado_cripto = cripto_numero.criptografar_numero(novo_dado)
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
                    while resposta not in ['S', 'N']:
                        print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")
                        resposta = input(f"Você usou {meio} hoje? (S/N): ").strip().upper()
                    new_resposta_transporte.append(resposta)
                novo_dado_str = "".join(new_resposta_transporte)
                novo_dado_cripto = cripto_texto.criptografar_texto(novo_dado_str)
                dado = 'meio_transporte_utilizado'
            case _:
                print("Opção inválida.")
                return
        
        cursor.execute(f"UPDATE monitoramento_sustentabilidade SET {dado} = %s WHERE data_monitoramento = %s", (novo_dado_cripto, data_cripto))
        conexao.commit()
        print(f"\nO dado {dado} do dia {data} foi alterado com sucesso!")


# ------- Função para média dados ----------
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
        id_reg, data_desc, agua_desc, kwh_desc, kg_lixo_desc, lixo_desc, transporte_desc = descriptografar_registro(linha)
        
        soma_agua += agua_desc
        soma_kwh += kwh_desc
        soma_lixo_kg += kg_lixo_desc
        soma_lixo_percent += lixo_desc
        
        transportes = list(transporte_desc)
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

# ========== CONEXÃO COM BANCO DE DADOS ==========
conexao = mysql.connector.connect(
    host="BD-ACD",
    user="BD180225124",
    password="Vzbbv5",
    database="BD180225124"
)
cursor = conexao.cursor()

# ========== MENU PRINCIPAL ==========
lobby = 10
while lobby != 0:
    print("\tMonitoriamento de Sustentabilidade")
    print("""
[ 1 ]. Avaliar Sustentabilidade
[ 2 ]. Editar Dados da Avaliação
[ 3 ]. Remover Avaliação
[ 4 ]. Registro Diário de Sustentabilidade
[ 5 ]. Consultar Média de Sustentabilidade
[ 6 ]. Consultar Dados por Data
[ 0 ]. Encerrar Sistema
""")
    try:
        lobby = int(input())
    except:
        print("Entrada inválida! Por favor, insira um número válido.")
        continue
    
    if lobby == 1:
        data, agua, kwh, kg_lixo, lixo, resposta_transporte = informacao_recebidas()
        consumo_agua, consumo_energia, consumo_porcentagem_reciclados, uso_transporte = calculo_sustentabilidade(agua, kwh, lixo, resposta_transporte)
        print(f"""\n\n---------RESULTADOS---------\n
CONSUMO ÁGUA: {agua} | SUSTENTABILIDADE: {consumo_agua}
KWH: {kwh} | SUSTENTABILIDADE: {consumo_energia}
LIXO: {lixo} | SUSTENTABILIDADE: {consumo_porcentagem_reciclados}
MEIOS_TRANSPORTE: {''.join(resposta_transporte)} | SUSTENTABILIDADE: {uso_transporte}
""")
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        try:
            lobby = int(input())
        except:
            lobby = 10
    elif lobby == 2:
        alteracao_dados()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        try:
            lobby = int(input())
        except:
            lobby = 10
    elif lobby == 3:
        apagar_todos_dados()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        try:
            lobby = int(input())
        except:
            lobby = 10
    elif lobby == 4:
        monitdiario()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        try:
            lobby = int(input())
        except:
            lobby = 10
    elif lobby == 5:
        media_monitoramento()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        try:
            lobby = int(input())
        except:
            lobby = 10
    elif lobby == 6:
        data_especifica()
        print("""
[ 1 ]. Retornar ao menu
[ 0 ]. Encerrar programa
""")
        try:
            lobby = int(input())
        except:
            lobby = 10

cursor.close()
conexao.close()

