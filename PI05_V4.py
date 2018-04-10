##____________________________BIBLIOTECAS______________________________________________##


import time;
import datetime
import requests;
import matplotlib;
from uclcoin import KeyPair, Transaction, Block
from matplotlib import pyplot as plt
from tkinter import *
from matplotlib import style
from time import sleep


##____________________________VARIÁVEIS_GLOBAIS_________________________________________##

style.use('ggplot');
url = 'https://moeda.ucl.br'
chv = '036122dfcca6e3f42dee13921b40c90a8a2eef2a1e655c424ac44d84d0d6acde8a';
graphic = [];
x = [0];
y = [0];
rank = [];
posicao = ['Primeiro', 'Segundo', 'Terceiro', 'Quarto', 'Quinto', 'Sexto', 'Sétimo','Oitavo', 'Nono', 'Demais Posições'];
cols = ['crimson', 'lightcoral', 'red', 'deepskyblue', 'fuchsia','olive', 'lightgray', 'plum', 'moccasin', 'orange']


##____________________________CLASSES_E_FUNÇÕES_________________________________________##

#Classe para Gerar Registro de Mineração#
class point:
    def __init__(self, indice, status, tempo, saldo):
        self.indice = indice;
        self.status = status;    
        self.tempo = tempo;
        self.saldo = saldo;

#Função para Inserir Registro de Mineração em uma Lista Global#        
def plotpoint(object):
    graphic.append(object);

#Função para Inserir Registro em Listas Globais Destinadas ao Gráfico de Evolução# 
def addpoint(k, j):
        x.append(k);
        y.append(j);

#Função que Retorna o Saldo de uma Chave Púplica# 
def balancekey(chave):    
        blc = requests.get(f'{url}/balance/{chave}');
        blc = blc.json();
        blc = int(blc['balance']);
        return blc;        


##____________________________MINERAÇÃO DE CRIPOMOEDAS_________________________##
    

#Função Mineração de Criptomoedas UCLCOIN# 
def opcMineracao(chave):

    inicio = fim = block_time = 0;
    max_iteration = 10000000;
    count_iteration = 0;    
    res = requests.get(f'{url}/block/minable/{chave}');
    res = res.json();
    dificuldade = res['difficulty'];
    block = res['block'];
    currentblock = block['index'];    
    print('Bloco para Mineração Carregado... \nÍndice: ', currentblock);
    block = Block.from_dict(block);
    print('\n... INICIANDO ...\n');
    
    inicio = time.time();    
    while (block.current_hash[:dificuldade].count('0') < dificuldade):
        block.nonce += 1;
        block.recalculate_hash();
        count_iteration = count_iteration + 1;
        
        if (count_iteration == max_iteration): 
            fim = time.time();
            block_time = int((fim - inicio)/60);
            addpoint(block_time, balancekey(chave));           
            count_iteration = 0;
            res = requests.get(f'{url}/block/minable/{chave}');
            res = res.json();
            requestedblock = res['block'];
            requestedblock = requestedblock['index'];
            
            try:
                print('...')
            except KeyboardInterrupt:
                return

            if (currentblock != requestedblock):
                block_point = point(currentblock, 'Perda', block_time, balancekey(chave));
                plotpoint(block_point);
                print('\nBloco Perdido, Iniciando novo Bloco!\n');              
                opcMineracao(chave);
        
               
    fim = time.time();
    block_time = int((fim - inicio)/60);    
    print('\n   Mineração do Bloco Finalizada!\nTempo Decorrido: ', block_time, ' min');
    res = requests.post(f'{url}/block', json = dict(block));
    
    if res.ok:
        print('\nMineração Aceita pela BlockChain!');
        addpoint(block_time, balancekey(chave));
        block_point = point(currentblock, 'Aceito', block_time, balancekey(chave) );
        plotpoint(block_point);
        
    else:
        print('\nMineração Rejeitada pela BlockChain!');        
        addpoint(block_time, balancekey(chave));
        block_point = point(currentblock, 'Rejeitado', block_time, balancekey(chave) );        
        plotpoint(block_point);
    opcMineracao(chave);
    

##____________________________DESENHO_DE_GRÁFICOS____________________________##
    

#Função para Gerar o Gráfico de Evolução de Mineração     
def evolution():
    plt.plot(x,y,'c',label='Chave Principal', linewidth=4);
    plt.title('Evolução na Mineração de Criptomoedas \nUCLOIN');
    plt.ylabel('Saldo de Criptomoedas -$-');
    plt.xlabel('Tempo -min-');
    plt.legend();
    plt.grid(True,color='k');
    plt.show();
    
#Função para Gerar o Gráfico de Ranking de Mineração 
def ranking():
    res = requests.get(f'{url}/ranking');
    res = res.json();
    resto = 0;    
    for i in range(len(res)):        
        if (i < 9):            
            pos = res[i];
            print(f'{i+1}º Posição, Chave: {pos[0]} \nTotal de Criptomoedas: {pos[1]} \n');
            rank.append(pos[1]);            
        else:
            pos = res[i];
            resto = pos[1] + resto;        
    rank.append(resto);   
    plt.pie (rank,
        labels = posicao,
        colors = cols,
        startangle = 90,
        shadow= True,
        explode=(0.1,0,0,0,0,0,0,0,0,0),
        autopct='%1.1f%%');
    plt.title('Gráfico de Rankeamento \nUCLCOIN');
    plt.show();


##____________________________INTERFACE______________________________________##

class Application:

    def __init__(self, master= None):

        ##DECLARAÇÃO_CONTAINER
        self.fontePadrao = ("Arial", "10");

        self.primeiroContainer = Frame(master);
        self.primeiroContainer["pady"] = 10;
        self.primeiroContainer["padx"] = 100;
        self.primeiroContainer["width"] = 200;
        
   
        self.segundoContainer = Frame(master);
        self.segundoContainer["pady"] = 10;
        self.segundoContainer["padx"] = 20;
        self.segundoContainer["width"] = 200;
        
   
        self.terceiroContainer = Frame(master);
        self.terceiroContainer["pady"] = 10;
        self.terceiroContainer["padx"] = 25;
        self.terceiroContainer["width"] = 200;
        
        self.quartoContainer = Frame(master);
        self.quartoContainer["pady"] = 10;
        self.quartoContainer["padx"] = 100;
        self.quartoContainer["width"] = 200;


        self.primeiroContainer.pack(side=TOP);
        self.quartoContainer.pack(side=BOTTOM);
        self.segundoContainer.pack(side=LEFT);   
        self.terceiroContainer.pack(side=RIGHT);
        


        ##PRIMEIRO_CONTAINER_OBJETOS
           
        self.titulo = Label(self.primeiroContainer, text="Minerador de Criptomoedas \n-PIV-");
        self.titulo["font"] = ("Times New Roman", "25", "bold");
        self.titulo.pack();

        ##SEGUNDO_CONTAINER_OBJETOS

        self.lbsaldo = Label(self.segundoContainer, text="Saldo Total", width=30);
        self.lbsaldo["font"] = ("Arial", "8", "bold");
        self.lbsaldo.pack();

        self.saldo = Label(self.segundoContainer, text="$ 00.0", width=30);
        self.saldo["font"] = ("Arial", "12", "bold");
        self.saldo.pack();

        self.nomeLabe1x = Label(self.segundoContainer,text="", font=self.fontePadrao);
        self.nomeLabe1x.pack();

        #BOTAO SALDO
        self.btsaldo = Button(self.segundoContainer);
        self.btsaldo["text"] = "Atualizar Saldo";
        self.btsaldo["font"] = ("Calibri", "8");
        self.btsaldo["width"] = 15;
        self.btsaldo["command"] = self.saldoatual;
        self.btsaldo.pack();
        

        ##TERCEIRO_CONTAINER_OBJETOS
        self.nomeLabe0 = Label(self.terceiroContainer,text="Chave Pública", font=self.fontePadrao);
        self.nomeLabe0.pack();
   
        self.chavep = Entry(self.terceiroContainer);
        self.chavep["width"] = 30;
        self.chavep["font"] = self.fontePadrao;
        self.chavep.pack();

        self.nomeLabe1 = Label(self.terceiroContainer,text="", font=self.fontePadrao);
        self.nomeLabe1.pack();
        
        #BOTAO MINERAR  
        self.minerar = Button(self.terceiroContainer);
        self.minerar["text"] = "Minerar";
        self.minerar["font"] = ("Calibri", "8");
        self.minerar["width"] = 15;
        self.minerar["command"] = self.mineracao;
        self.minerar.pack(side=LEFT, anchor=NW);
   
        #BOTAO CANCELAR
        self.cancelar = Button(self.terceiroContainer);
        self.cancelar["text"] = "Cancelar";
        self.cancelar["font"] = ("Calibri", "8");
        self.cancelar["width"] = 15;
        self.cancelar["command"] = self.cancelar;
        self.cancelar.pack(side=RIGHT, anchor=NE);


        ##QUARTO_CONTAINER_OBJETOS
        self.nomeLabe2 = Label(self.quartoContainer,text="GRÁFICOS", font=self.fontePadrao, width=34);
        self.nomeLabe2.pack();

        self.nomeLabe3 = Label(self.quartoContainer,text="", font=self.fontePadrao);
        self.nomeLabe3.pack(side=BOTTOM);

        #BOTAO GRÁFICO DE EVOLUÇÃO
        self.graf01 = Button(self.quartoContainer);
        self.graf01["text"] = "GRAFICO - Evolução";
        self.graf01["font"] = ("Calibri", "8");
        self.graf01["width"] = 20;
        self.graf01["command"] = self.gfc01;
        self.graf01.pack(side=LEFT, anchor=NE);
   
        #BOTAO GRAFICO DE RANKING
        self.graf02 = Button(self.quartoContainer);
        self.graf02["text"] = "GRAFICO - Ranking";
        self.graf02["font"] = ("Calibri", "8");
        self.graf02["width"] = 20;
        self.graf02["command"] = self.gfc02;
        self.graf02.pack(side=RIGHT, anchor=NW);

 

   
##_____________________________METÓDO_INTERFACE___________________________________##   
    
    def mineracao(self):
        chavepublica = self.chavep.get();
        try:
            if chavepublica == '':                
                print('Minerando com Chave Padrão');    
                opcMineracao(chv);
            else:
                print(f'Minerando com a Chave Digitada: {chavepublica}');
                opcMineracao(chavepublica);
        except ValueError:
            print('Chave Inválida');
    def cancelar(self):
        print('Sem Implementação');
       
    def gfc01(self):
        evolution();
        
    def gfc02(self):
        ranking();

    def saldoatual(self):        
        chavepublica = self.chavep.get();
        try:
            if chavepublica == '':
                self.nomeLabe1x["text"] = "Usando Chave Padrão";
                b = float(balancekey(chv));
                print(b);
                self.saldo["text"] = f"$ {b}";

            else:
                b = float(balancekey(chavepublica));
                self.nomeLabe1x["text"] = "Usando Chave Digitada";
                self.saldo["text"] = f"$ {b}";
                
        except ValueError:
            self.nomeLabe1x["text"] = "Chave Inválida";
            print('Chave Inválida');
         
##INSTACIAÇÃO DE INTERFACE##
root = Tk();
root.geometry("700x400+500+100");

Application(root);
root.mainloop();
