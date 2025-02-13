from flask import Flask, redirect, render_template, request, url_for, render_template_string

app = Flask(__name__)

var = []
acertos = 0
cor_1 = 'rgb(224, 243, 250)'
cor_2 = 'rgb(224, 243, 250)'
cor_3 = 'rgb(224, 243, 250)'
cor_4 = 'rgb(224, 243, 250)'
cor_5 = 'rgb(224, 243, 250)'

texto = ''

# >>> Novas estruturas para as regras solicitadas <<<
selected_cards = set()      # Cards que já foram clicados (não deixa repetir)
highlight_cards = set()     # Cards que estão sendo selecionados no momento (até fechar grupo de 5)
completed_categories = set()# Categorias que já pontuaram

@app.route('/', methods=['GET', 'POST'])
def index():
    global var, cor_1, cor_2, cor_3, cor_4, cor_5
    global acertos, texto
    global selected_cards, highlight_cards, completed_categories

    cor_muda = False
    
    # Verifica se há parâmetro para reiniciar
    reinicia_flag = request.args.get('reinicia', 'false').lower() == 'true'
    if reinicia_flag:
        var = []
        acertos = 0
        cor_1 = 'rgb(224, 243, 250)'
        cor_2 = 'rgb(224, 243, 250)'
        cor_3 = 'rgb(224, 243, 250)'
        cor_4 = 'rgb(224, 243, 250)'
        cor_5 ='rgb(224, 243, 250)'
        texto = ''

        # >>> Zera sets/dicionários novos <<<
        selected_cards.clear()
        highlight_cards.clear()
        completed_categories.clear()

        return redirect(url_for('index'))

    if request.method == 'POST':
        cor = request.form['palavra']      # Categoria (linha1, linha2, etc.)
        card_id = request.form['card_id']  # ID único do card

        # 1) Checa se já clicou antes no mesmo card
        if card_id in selected_cards:
            texto = '<h3 style="color: red; font-weight:800;">Você já clicou este card!</h3>'
            return render_template('index.html',
                                   cor_1=cor_1,
                                   cor_2=cor_2,
                                   cor_3=cor_3,
                                   cor_4=cor_4,
                                   cor_5=cor_5,
                                   texto=texto,
                                   acertos=acertos,
                                   cor_muda=cor_muda,
                                   highlight_cards=highlight_cards)
        
        # 2) Caso seja a primeira vez nesse card, registra
        selected_cards.add(card_id)
        highlight_cards.add(card_id)
        var.append(cor)

        # Checa se o grupo de 5 foi completo
        if len(var) ==4 :
            # Verifica se todos são iguais
            if var[0] == var[1] == var[2] == var[3]:
                # Pega a categoria
                categoria = var[0]

                # Verifica se já pontuou essa categoria antes
                if categoria not in completed_categories:
                    acertos += 1
                    completed_categories.add(categoria)
                    texto = '<h3 style="color: green; font-weight:800;">Acertou</h3>'

                    # Muda a cor conforme a categoria
                    if categoria == 'linha1':
                        cor_1 = '#F8C8DC'
                    elif categoria == 'linha2':
                        cor_2 = '#A7C7E7'
                    elif categoria == 'linha3':
                        cor_3 = '#FFF9B6'
                    elif categoria == 'linha4':
                        cor_4 = '#D8BFD8'
                    elif categoria == 'linha5':
                        cor_5 = 'lightgreen'
                else:
                    # Já concluiu essa categoria antes
                    texto = '<h3 style="color: orange; font-weight:800;">Você já completou essa categoria!</h3>'

            else:
                # Errou: remover destaque desses 5 cards
                texto = '<h3 style="color: red; font-weight:800;">Errou</h3>'
                # Precisamos liberar esses 4 do selected_cards e highlight_cards
                # Assim o usuário pode clicar neles novamente
                for i in range(4):
                    # var[i] é a categoria, mas precisamos do ID correspondente
                    # Entretanto, não armazenamos o ID junto da categoria
                    # => Usaremos a lista highlight_cards temporária
                    # Mas highlight_cards tem todos. Precisamos só dos últimos 5
                    # Uma forma simples: remover todos, pois esses 5 são os únicos no highlight
                    # Se quisermos ser exatos: guardamos a lista de IDs no momento
                    pass

                # Forma simples: limpamos selected_cards e highlight_cards dos últimos 5
                # Precisamos sabermos quais 5 IDs correspondem a var...
                # Uma opção é armazenar (cor, card_id) em var, mas para não mexer demais,
                # podemos apenas limpar *todos* do highlight_cards, pois nesse jogo
                # estamos selecionando 5 de cada vez. Mas se há seleções anteriores corretas
                # no highlight_cards? Normalmente ficaria vazio, pois limpamos depois do acerto.
                
                # Solução simples: armazenar tuplas (categoria, card_id) em var
                # ou fazer um "last5_ids" separado. A seguir está o jeito mais fácil:
                
                # Aqui vamos criar uma cópia do highlight_cards,
                # pois ele contém *todos* os que foram selecionados até agora
                # e não removidos. Mas só removemos os que foram selecionados neste turno
                # (os 5 últimos). Então:
                #   1) Descobrimos quais 5 card_ids foram adicionados nesse turno
                #   2) Removemos do selected_cards e do highlight_cards
                # Para isso, basta armazenar (categoria, card_id) em var, mas
                # vamos adaptar agora sem remover linhas antigas:

                texto = '<h3 style="color: red; font-weight:800;">Errou</h3>'
            
            # Depois de conferir, limpamos a seleção
            # Nesse momento, precisamos remover do selected_cards
            # os 5 últimos que foram clicados *se* deu erro.
            if 'Errou' in texto:
                # Precisamos remover apenas os 5 últimos IDs.
                # Para isso, podemos usar reversed(highlight_cards) ou armazenar numa lista
                # MAS highlight_cards é um set() => não garante ordem
                # Solução: crie uma lista "temp" para os 5 últimos
                # A forma mais simples é armazenar (cor, card_id) em outra lista global
                # MAS sem mudar muito o seu código, iremos "zerar" highlight_cards e selected_cards
                # dos 5 últimos. Vamos supor que a cada jogo (5 cliques) não existia highlight pendente.
                # Então "highlight_cards" só tem esses 5. No caso de acerto, limpamos tudo.
                # No caso de erro, limpamos esses 5. Assim:

                # Copie highlight_cards antes de resetar var
                # (mas lembre que highlight_cards pode ter mais que 5 se o usuário errou e clicou de novo)
                # Vamos fazer algo simples: se len(var) == 5 => esses 5 são todos os destaques recentes.
                
                # Precisamos realemente rastrear IDs "por clique".
                # Aqui vai a implementação prática e simples:
                texto = '<h3 style="color: red; font-weight:800;">Errou</h3>'
                # Vamos apenas limpar *todos* highlight_cards recém-adicionados
                # se seu "palavra" (categoria) é a que está em var? Nem sempre.
                # Para não complicar, vamos esvaziar highlight_cards completamente
                # e também remover esses IDs de selected_cards, pois o usuário pode reclicar.
                
                for cid in highlight_cards:
                    if cid in selected_cards:
                        selected_cards.remove(cid)
                highlight_cards.clear()

            # Se acertou ou completou, de qualquer forma limpamos highlight_cards
            # pois não queremos manter seleção
            if 'Acertou' in texto or 'completou' in texto:
                highlight_cards.clear()

            # Fim do grupo de 5, limpamos var
            var = []

        else:
            # Ainda não chegou em 5 cliques
            texto = render_template_string(f'<h3>Itens selecionados : {len(var)}</h3>')

        # Verifica se já ganhou o jogo
        if acertos == 5:
            var = []
            texto = '<button style="width: 100%; background-color: green; height:40px; color: white;font-weight: 800;">Você ganhou o jogo!</button>'

        return render_template('index.html',
                               cor_1=cor_1,
                               cor_2=cor_2,
                               cor_3=cor_3,
                               cor_4=cor_4,
                               cor_5=cor_5,
                               texto=texto,
                               acertos=acertos,
                               cor_muda=cor_muda,
                               highlight_cards=highlight_cards)

    # GET request inicial
    return render_template('index.html',
                           cor_1=cor_1,
                           cor_2=cor_2,
                           cor_3=cor_3,
                           cor_4=cor_4,
                           cor_5=cor_5,
                           texto=texto,
                           acertos=acertos,
                           highlight_cards=highlight_cards)

@app.route('/regras', methods=['GET','POST'])
def regras():
    return render_template('regras.html')

@app.route('/reinicia')
def reinicia():
    reinicia_flag = True
    return redirect(url_for('index', reinicia=reinicia_flag))

if __name__ == "__main__":
    app.run(debug=True)