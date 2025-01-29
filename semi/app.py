from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

var = []
acertos = 0
cor_verde='beige'
cor_amarelo='beige'
cor_vermelho='beige'
texto=''
@app.route('/',methods=['GET','POST'])
def index():
    global var
    global cor_verde
    global cor_amarelo
    global cor_vermelho
    global acertos
    global texto

    if request.method=='POST':
        cor = request.form['cor']
        
        if len(var)>=2:
            var = []
        var.append(cor)
           
        if len(var)==2 :
            if var[0]==var[1]:
                acertos +=1
                texto='Acertou'
                if var[0]=='verde':
                    cor_verde = 'green'
                elif var[0]=='vermelho':
                    cor_vermelho = 'red'
                elif var[0]=='amarelo':
                    cor_amarelo = 'yellow'
            elif var[0] != var[1]:
                texto='Errou'
        if acertos>=3:
            acertos=0
            texto = 'Voce gahou o jogo!'
            proximo = 'Próximo'
        return render_template('index.html',cor_verde=cor_verde,cor_amarelo=cor_amarelo,cor_vermelho=cor_vermelho, texto=texto, proximo=proximo)
    return render_template('index.html')    
            
