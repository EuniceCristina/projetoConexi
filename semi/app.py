from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

var = []
acertos = 0
cor_1='rgb(224, 243, 250)'
cor_2='rgb(224, 243, 250)'
cor_3='rgb(224, 243, 250)'
cor_4='rgb(224, 243, 250)'
cor_5='rgb(224, 243, 250)'
texto=''

@app.route('/',methods=['GET','POST'])
def index():
    global var
    global cor_1
    global cor_2
    global cor_3
    global cor_4
    global cor_5
    global acertos
    global texto
    

    if request.method=='POST':
        cor = request.form['palavra']
        
        if len(var)==5:
            var = []
        
        var.append(cor)
           
        if len(var)==5 :
            
            if var[0]==var[1] and var[1]==var[2] and var[2]==var[3] and var[3]==var[4]:
                acertos +=1
                var = []
                texto='Acertou'
                if cor =='linha1':
                    cor_1 = '#F8C8DC'
                elif cor =='linha2':
                    cor_2 = '#A7C7E7'
                elif cor =='linha3':
                    cor_3 = '#FFF9B6'
                elif cor =='linha4':
                    cor_4 = '#D8BFD8'
                elif cor =='linha5':
                    cor_5 = '#FFD3B6'
            else:
                texto='Errou'
        else:
            texto=f'Itens selecionados : {len(var)}'
        if acertos==5:
            var = []
            
           
            
            
            texto = 'Voce ganhou o jogo! '
           
        return render_template('index.html',cor_5=cor_5,cor_4=cor_4,cor_3=cor_3,cor_2=cor_2,cor_1=cor_1, texto=texto, acertos=acertos)
    
    return render_template('index.html')    
            