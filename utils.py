import gensim


## Tamil
def get_tamil_model():
        
    TAMIL_MODEL = {}
    similars_lines = open('./resources/ta/similar.tsv').readlines()
    dissimilars_lines = open('./resources/ta/dissimilar.tsv').readlines()
    for sline, dline in zip(similars_lines, dissimilars_lines):
        sim, dis = [], [] 
        sline = sline.split('|')
        dline = dline.split('|')
        word = sline[0]
        for i, j in zip(sline[1:], dline[1:]):
            sim.append([i])
            dis.append([j])

        TAMIL_MODEL[word] = {
                'similar': sim[:10],
                'not_similar': dis[:10]
            }
            
        

    return TAMIL_MODEL

def get_malayalam_model():
    model = gensim.models.Word2Vec.load("./resources/ml/model/word2vec_gensim")
    return model

