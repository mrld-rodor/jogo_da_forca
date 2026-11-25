# palavras.py
# Estrutura: { "dificuldade": { "PALAVRA": ["dica 1", "dica 2"], ... } }

BANCO_PALAVRAS = {
    "facil": {
        "CASA":     ["Lugar onde você mora", "Tem telhado e porta"],
        "GATO":     ["Animal doméstico que mia", "Tem bigodes e gosta de peixe"],
        "BOLA":     ["Usada em esportes", "É redonda e rola"],
        "LIVRO":    ["Tem páginas e capa", "Fonte de conhecimento"],
        "MESA":     ["Móvel com tampo e pernas", "Usada para refeições"],
        "FACA":     ["Utensílio de cozinha", "Serve para cortar"],
        "FLOR":     ["Parte colorida da planta", "Tem pétalas"],
        "PEIXE":    ["Animal aquático", "Tem escamas e barbatanas"],
        "SAPO":     ["Anfíbio que pula", "Vive perto de lagoas"],
        "UVA":      ["Fruta em cachos", "Usada para fazer vinho"],
        "SINO":     ["Objeto que faz som", "Fica em torres de igreja"],
        "RATO":     ["Roedor pequeno", "Tem rabo comprido"],
        "AMOR":     ["Sentimento profundo", "Representado por coração"],
    },
    "normal": {
        "BANANA":   ["Fruta amarela e alongada", "Macacos adoram"],
        "JANELA":   ["Abertura para o exterior", "Deixa entrar luz"],
        "CAVALO":   ["Animal grande e veloz", "Usado para montar"],
        "ESCOLA":   ["Lugar de aprendizado", "Tem professores e alunos"],
        "FUTEBOL":  ["Esporte mais popular do Brasil", "Jogado com bola nos pés"],
        "ELEFANTE": ["Animal muito grande", "Tem tromba"],
        "GIRAFA":   ["Animal de pescoço longo", "Vive na África"],
        "CACHORRO": ["Melhor amigo do homem", "Late e abana o rabo"],
        "TELEFONE": ["Aparelho de comunicação", "Toca quando alguém liga"],
        "XADREZ":   ["Jogo de tabuleiro", "Reis, damas e peões"],
        "MONTANHA": ["Grande elevação natural", "Desafio para alpinistas"],
        "BICICLETA":["Veículo de duas rodas", "Movida a pedal"],
        "PIPOCA":   ["Petisco de cinema", "Feita de milho"],
    },
    "dificil": {
        "CONSTRANGIMENTO": ["Situação de vergonha", "Pode causar rubor"],
        "INDIVIDUALIDADE": ["Característica única de cada um", "Diferencia as pessoas"],
        "INTERDEPENDENTE": ["Que depende um do outro", "Relação de mutualidade"],
        "SENSACIONALISMO": ["Exagero na divulgação de notícias", "Comum em tabloides"],
        "INEXORAVELMENTE": ["De forma implacável", "Sem chance de escape"],
        "HIPOTETICAMENTE": ["De maneira suposta", "Baseado em hipótese"],
        "CARACTERISTICAS": ["Traços marcantes", "Atributos de algo ou alguém"],
        "RECRUDESCIMENTO": ["Aumento da intensidade", "Agravação de uma situação"],
        "DELIBERADAMENTE": ["De forma intencional", "Com propósito claro"],
        "POLITRAUMATISMO": ["Múltiplas lesões no corpo", "Termo médico de trauma grave"],
        "SUSCETIBILIDADE": ["Facilidade de ser afetado", "Sensibilidade a algo"],
        "SUPRAMENCIONADO": ["Citado anteriormente", "Referido acima"],
    },
    "secreta": {
        "PNEUMOULTROMICROSCOPICOSILIVULCANOCONIOTICO": [
            "Doença pulmonar ocupacional", "Causada por poeira de minas"
        ],
        "PARACLOROBENZILPIRROLIDINONETILBENZIMIDAZOL": [
            "Nome químico muito longo", "Composto farmacêutico"
        ],
        "PIPERIDINOETOXICARBOMETOXIBENZOFENONA": [
            "Termo químico complexo", "Composto orgânico sintético"
        ],
        "TETRABROMETACRESOLSULFONOFTALEINA": [
            "Indicador ácido-base", "Nome de corante laboratorial"
        ],
        "ANTICONSTITUCIONALISSIMAMENTE": [
            "De modo contrário à Constituição", "Advérbio de modo longo"
        ],
        "HIPOPOTOMONSTROSESQUIPEDALIOFOBIA": [
            "Medo de palavras longas", "Fobia curiosa"
        ],
    },
}