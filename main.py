# Sistema criado para treinar uma IA, com intuito de fazer ela acertar qual nume-
# ro não aparecera nos proximos 5 numeros ou segundos
# Sistema criado a partir do video do "LIRA HASTAG-IA jogando FLAPPY BIRD", mas totalmente modificado por PHILLIP DYLAN
# reutilizei somente o metodo de como colocar a IA no sistema

# IMPORTANTE INSTALAR A BIBLIOTECA PIP ****NEAT-PYTHON*****
import pygame
import neat
import os
import random
import schedule
from random import randint


ai_jogando = True
geracao = 0

TELA_LARGURA = 1300
TELA_ALTURA = 700

class IaJogando:
    def __init__(self):
        self.x = randint(40, 900)
        self.y = randint(50, 640)
        self.valor_inicial = 0
        self.trocar = False
        self.entar = False
        self.contagem = 0
        self.verificando = False
        self.iniciar_contagem = False
        self.iniciar_entrada = False
        self.perda = 0
        self.ganho = 0
        self.confirmado = False
        self.possivel_ganho = 0
        self.perda_total = 0
        self.fora = False
        self.reiniciar = False
        self.regresiva = 50
        self.entrou_durante_contagem = 0

# Mostra na tela os dados atuais da ia
# NUMERO - numero que ela esta usando como previsão
# Ganho - quantas vezes ela previu certo e ganhou
# Contagem - depois de ela confirmar a entrada com o numero da previsão é iniciado os 5 segundos
# Regressiva - quanto tempo ela pode ficar sem entrar pelo menos uma vez ainda
# entrou contagem - se ela entrou durante o tempo que ela tem para poder entrar
# fora - se ela ultrapassou o numero de perdas aceitavel ela é tirada da tela
    def desenhar(self,tela):
        texto1 = fonte.render(f"previsão: {self.valor_inicial}: ganho: {self.ganho}: contagem {self.contagem}", 1, (255, 255, 255))
        tela.blit(texto1, (self.x, self.y))
        texto2 = fonte.render(f"fora: {self.fora},regressiva: {self.regresiva}: entrou contagem {self.entrou_durante_contagem} ",1, (255, 255, 255))
        tela.blit(texto2, (self.x, self.y + 8))

# se ela nao entrar durante o tempo que falta ela é tirada da tela
    def regressiva_perder(self):
        if self.regresiva == 0 and self.entrou_durante_contagem == 1:
            self.entrou_durante_contagem = 0
            self.regresiva = 50
        if self.regresiva == 0 and self.entrou_durante_contagem == 0:
            self.fora = True

    def regressiva_contar(self):
        if self.regresiva > 0:
            self.regresiva -=  1

    def trocar_valor(self):
        if self.entar == False:
            self.trocar = True

    def bloqueio(self):
        self.trocar = False

# Fazer troca acima trocar o numero da previsão por um numero acima do atual se 1 vai para 2
    def fazer_troca_cima(self):
        if self.trocar == True:
            self.valor_inicial += 1
        if self.valor_inicial > 9:
            self.valor_inicial = 0

# Fazer troca acima trocar o numero da previsão por um numero abaixo do atual se 1 vai para 0
    def fazer_troca_baixo(self):
        if self.trocar == True:
            self.valor_inicial -= 1
        if self.valor_inicial < 0:
            self.valor_inicial = 9

# Ia faz a entrada acreditando que os proximos 5 numeros nao serao o da previsão
    def fazer_entrada(self):
            if self.contagem > 0:
                self.entrar = False
                self.iniciar_entrada = False
                self.trocar = False
            elif self.contagem == 0:
                self.entar = True
                self.contagem = 5
                self.iniciar_entrada = True
                self.possivel_ganho = 0
                self.entrou_durante_contagem = 1

# depois de fazer a entrada faz uma contagem de 5 segundos que é o tempo de aparecer o proximos 5 numeros
    def diminuir_contador(self):
        if self.contagem > 0:
            self.contagem -= 1

# faz a verificaçao se a Ia fizer a entrada ela nao pode alterar o numero de previsão ate acabar os 5 segundos
    def fazer_verificacao1(self):
        if self.contagem == 0:
            self.confirmado = False
            self.trocar = True
        elif self.contagem > 0:
            self.confirmado = True
            self.trocar = False

# Faz a verificação se durante os proximos 5 segundos o numero que a Ia previu aparce
    def fazer_verificacao_entrada(self):
        with open("dados.txt") as dado:
            continuacao = True
            while continuacao:
                try:
                    data = int(dado.readlines()[0])
                    continuacao = False
                except:
                    print("An exception occurred")
                    continuacao = True
        self.ultimo_numero = data
        if self.valor_inicial == self.ultimo_numero and self.confirmado == True:
            self.perda += 1
            self.possivel_ganho = 0
            self.contagem = 0
        if self.confirmado == True and self.valor_inicial != self.ultimo_numero:
            self.possivel_ganho += 1
        if self.perda == 1:
            self.perda_total += 1
            self.fora = True
        if self.possivel_ganho >= 4:
            self.possivel_ganho = 0
            self.ganho += 1

# area para contar quantas vezes o numero apareceu a envira para a Ia fazer o calculo
# faz a verificação a partir do arquivo dado.txt-
# que é gerado apenas 1 numero aleatorio em uma unica linha do aruivo dados.txt
class Numeros:
    def __init__(self):
        self.ultimo_numero = 0
        self.lista_ultimos_numeros = []
        self.x = 10
        self.y = 20
        self.zero = 0
        self.um = 0
        self.dois = 0
        self.tres = 0
        self.quatro = 0
        self.cinco = 0
        self.seis = 0
        self.sete = 0
        self.oito = 0
        self.nove = 0

    def retornar_numeros(self):
        self.zero = self.lista_ultimos_numeros.count(0)
        self.um = self.lista_ultimos_numeros.count(1)
        self.dois = self.lista_ultimos_numeros.count(2)
        self.tres = self.lista_ultimos_numeros.count(3)
        self.quatro = self.lista_ultimos_numeros.count(4)
        self.cinco = self.lista_ultimos_numeros.count(5)
        self.seis = self.lista_ultimos_numeros.count(6)
        self.sete = self.lista_ultimos_numeros.count(7)
        self.oito = self.lista_ultimos_numeros.count(8)
        self.nove = self.lista_ultimos_numeros.count(9)

# ultimo numero e ultimos 50 numeros que apareceram no arquivo dados.txt
    def desenhar(self,tela):
        texto_principal = fonte.render(f"ultimo numero: {self.ultimo_numero}: ultimos 50 numeros: {self.lista_ultimos_numeros}",1,(255, 255, 255))
        tela.blit(texto_principal, (self.x, self.y))
    def pegar_ultimo_numero(self):
        with open("dados.txt") as dado:
            continuacao = True
            while continuacao:
                try:
                    data = int(dado.readlines()[0])
                    continuacao = False
                except:
                    print("An exception occurred")
                    continuacao = True
            self.ultimo_numero = data

    def criando_lista(self):
        self.lista_ultimos_numeros.insert(0, self.ultimo_numero)
        if len(self.lista_ultimos_numeros) > 49:
            self.lista_ultimos_numeros.pop()

pygame.init()
pygame.font.init()
fonte = pygame.font.SysFont('arial',10,True,True)

# parte usada para gerar os numeros aleatorios e enviar para o arquivo que é utilizado dados.txt
def gerar_numeros_aleatorios_no_arquivo_dados():
    arquivo = open('dados.txt', 'w')
    numeros_em_str = random.randrange(0, 10)
    numero_em_str = str(numeros_em_str)
    arquivo.write(numero_em_str)
    arquivo.close()

def desenhar_tela(tela, iasjogando,numeros,maior_ponto,quantidade_ias_atualizando):
    for iaJogando in iasjogando:
        iaJogando.desenhar(tela)

    texto_principal = fonte.render(f"maior ponto: {maior_ponto}: IAs ativas: {quantidade_ias_atualizando}", 1, (255, 255, 255))
    tela.blit(texto_principal, (20,60 ))

    if ai_jogando:
        texto_principal = fonte.render(f"Geração: {geracao}", 1,(255, 255, 255))
        tela.blit(texto_principal, (20, 35))


    numeros.desenhar(tela)
    pygame.display.update()


def main(genomas, config):
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        lista_genomas = []
        iasjogando = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            iasjogando.append(IaJogando())

    else:
        iasjogando = [IaJogando()]
    numeros = Numeros()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    ponto = []

    relogio = pygame.time.Clock()
    pygame.display.set_caption('Teste AI')
    schedule.every(1).seconds.do(numeros.pegar_ultimo_numero)
    schedule.every(1).seconds.do(numeros.criando_lista)
    schedule.every(1).seconds.do(numeros.retornar_numeros)
    schedule.every(1).seconds.do(gerar_numeros_aleatorios_no_arquivo_dados)
    for i, iajogando in enumerate(iasjogando):
        schedule.every(1).seconds.do(iajogando.diminuir_contador)
        schedule.every(1).seconds.do(iajogando.regressiva_contar)
        schedule.every(1).seconds.do(iajogando.fazer_verificacao_entrada)

    rodando = True

    while rodando:
        relogio.tick(30)
        tela.fill((0, 0, 0))
        schedule.run_pending()


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w:
                        for iajogando in iasjogando:
                            iajogando.fazer_troca_cima()
                    elif evento.key == pygame.K_s:
                        for iajogando in iasjogando:
                            iajogando.fazer_troca_baixo()
                    elif evento.key == pygame.K_SPACE:
                        for iajogando in iasjogando:
                            iajogando.fazer_entrada()

        if len(iasjogando) <= 0:
            rodando = False
            break

        for i, iajogando in enumerate(iasjogando):
            if iajogando.regresiva > 0:
                lista_genomas[i].fitness += 0.0001
            output = redes[i].activate((abs(iajogando.valor_inicial), abs(numeros.ultimo_numero), abs(iajogando.regresiva),abs(numeros.zero),abs(numeros.um),abs(numeros.dois),abs(numeros.tres),abs(numeros.quatro),abs(numeros.cinco),abs(numeros.seis),abs(numeros.sete),abs(numeros.oito),abs(numeros.nove)))
            if output[0] > 0.5:
                iajogando.fazer_entrada()
            output = redes[i].activate((abs(iajogando.valor_inicial), abs(numeros.ultimo_numero), abs(iajogando.regresiva),abs(numeros.zero),abs(numeros.um),abs(numeros.dois),abs(numeros.tres),abs(numeros.quatro),abs(numeros.cinco),abs(numeros.seis),abs(numeros.sete),abs(numeros.oito),abs(numeros.nove)))
            if output[0] > 0.5:
                iajogando.fazer_troca_cima()
            output = redes[i].activate((abs(iajogando.valor_inicial), abs(numeros.ultimo_numero), abs(iajogando.regresiva),abs(numeros.zero),abs(numeros.um),abs(numeros.dois),abs(numeros.tres),abs(numeros.quatro),abs(numeros.cinco),abs(numeros.seis),abs(numeros.sete),abs(numeros.oito),abs(numeros.nove)))
            if output[0] > 0.5:
                iajogando.fazer_troca_baixo()

        for i, iajogando in enumerate(iasjogando):
            if iajogando.contagem > 0:
                lista_genomas[i].fitness += 0.05
                iajogando.bloqueio()
            schedule.run_pending()
            iajogando.fazer_verificacao1()
            iajogando.regressiva_perder()
            if iajogando.fora == True:
                iasjogando.pop(i)
                if ai_jogando:
                    lista_genomas[i].fitness -= 0.5
                    lista_genomas.pop(i)
                    redes.pop(i)
            ponto.insert(i, iajogando.ganho)

        for i, iajogando in enumerate(iasjogando):
            if iajogando.possivel_ganho == 4:
                lista_genomas[i].fitness += 0.10

        for i, iajogando in enumerate(iasjogando):
            if iajogando.ganho == 5 or iajogando.ganho == 10 or iajogando.ganho == 15 or iajogando.ganho == 20 or iajogando.ganho == 25 :
                lista_genomas[i].fitness += 0.10

        maior_ponto = max(ponto)
        quantidade_ias_atualizando = len(iasjogando)


        desenhar_tela(tela, iasjogando,numeros,str(maior_ponto),str(quantidade_ias_atualizando))

def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,caminho_config)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main)
    else:
        main(None,None)


if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'Config.txt')
    rodar(caminho_config)