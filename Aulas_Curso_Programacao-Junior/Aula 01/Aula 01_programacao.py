from random import randint

print("Olá vamos jogar um game?")
jogador = int(input("Advinhe o número que pensei: [De 1 à 5]: "))
computador = randint(1,5)
while True:
    if jogador == computador:
        print(f"Parabéns vc acertou o numero que escolhi foi {computador}")

    else:
        print(f"Que pena vc perdeu eu escolhi {computador} e vc {jogador}")
    continuar = input("Deseja continuar? [S/N]: ")
    if continuar in "Nn":
        break
        
print("Fim do game")

