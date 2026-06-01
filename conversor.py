import requests

#Função que conecta na API e busca a cotação atual da moeda desejada em relação ao Real (BRL).
def obter_cotacao(moeda):
    url = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL" #porque f? ##
    try:
        #Faz requisição para o site | O que está sendo requisitado? ##
        resposta = requests.get(url)
        #Transforma a resposta do site em um dicionário Python
        dados = resposta.json()

        #A API retorna a chave combinada, ex: 'USDBRL'
        chave_moeda = f"{moeda}BRL"

        #Pega o valor da compra ('bid') e transforma em número decimal (float)
        cotacao = float(dados[chave_moeda]['bid']) #O que é bid? ##
        nome_moeda = dados[chave_moeda]['name'].split('/')[0]

        return cotacao, nome_moeda
    
    except Exception as e:
        print(f"Erro ao buscar a cotação: {e}")
        return  None, None
    
def main():
    print("=== CONVERSOR DE MOEDAS EM TEMPO REAL ===")
    print("Opções de moedas para converter para Real (BRL):")
    print("1 - Dólar (USD)")
    print("2 - Euro (EUR)")
    print("3 - Bitcoin (BTC)")

    opcao = input("Escolha e informe o número da opção desejada: ")

    #Define o código da moeda com base na escolha do usuário
    if opcao == '1':
        moeda_escolhida = 'USD'
    elif opcao == '2':
        moeda_escolhida = 'EUR'
    elif opcao == '3':
        moeda_escolhida == 'BTC'
    else:
        print("Opção inválida!")
        return
    
    #Busca a cotação na internet
    cotacao, nome = obter_cotacao(moeda_escolhida) #Porque o uso da virgula e "cotacao, nome"? ##

    if cotacao:
        print(f"\nCotação atual do {nome}: R${cotacao: .2f}")

        #Pede o valor que o usuário quer converter
        try:
            quantidade = float(input(f"Quantos {moeda_escolhida} você deseja converter para BRL? "))
            total_reais = quantidade * cotacao
            print(f"\n{quantidade} {moeda_escolhida} equivale a: R$ {total_reais:.2f}")

        except ValueError:
            print("Por favor, digite um número válido para a quantidade.")

#Garante que o programa só rode se for executado diretamente
if __name__ == "__main__":
    main()


