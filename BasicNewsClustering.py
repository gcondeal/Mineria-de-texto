import re, pprint, os, numpy
import nltk
import sys
import string
from textblob import TextBlob
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from sklearn.metrics.cluster import *
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import adjusted_rand_score
from bs4 import BeautifulSoup, Comment
import re

# def read_file(file):
#     myfile = open(file,"r")
#     data = ""
#     lines = myfile.readlines()
#     for line in lines:
#         data = data + line
#     myfile.close
#     return data

def cluster_texts(texts, clustersNumber, distance):
    #Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of", len(collection), "terms.")

    #get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))

    ### And here we actually call the function and create our array of vectors.
    vectors = [numpy.array(TF(f,unique_terms, collection)) for f in texts]
    print("Vectors created.")

    # initialize the clusterer
    clusterer = AgglomerativeClustering(n_clusters=clustersNumber,
                                      linkage="average", affinity=distanceFunction)
    try:
        clusters = clusterer.fit_predict(vectors)
    except:
        print(sys.exc_info())
    return clusters

# Function to create a TF vector for one document. For each of
# our unique words, we have a feature which is the tf for that word
# in the current document
def TF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        try:
            word_tf.append(collection.tf(word, document))
        except:
            print(word + " ---- ")
    return word_tf

def tratamientoHTML(folderOrigen, folderDestino):
    listing = os.listdir(folderOrigen)

    for file in listing:
        if file.endswith(".html"):
            print(file)
            f = open(folderOrigen+"/"+file)
            bsObj = BeautifulSoup(f, "html.parser")
            f.close()

            cad_inicio = None
            cad_fin = None

            origen = bsObj.find(text=lambda text:isinstance(text, Comment))
            if "saved from url" in origen: # puedo identificar desde donde se ha descargado la página
                hayQueTratar = False
                titulo = None
                subtitulo = None
                objBody = None

                cad_inicio = '/* dynamic basic css */'
                cad_fin = 'OBR.extern.researchWidget();'

                if "www.theguardian.com" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'class' : 'content__headline'}).text
                    objBody = bsObj.find('div', attrs={'itemprop' : 'articleBody'})

                elif "www.telegraph.co.uk" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'itemprop' : 'headline name'}).text
                    objBody = bsObj.find('article', attrs={'itemprop': 'articleBody'})
                    cad_inicio = '/* dynamic basic css */'
                    cad_fin = 'OBR.extern.researchWidget();'

                elif "www.abc.es" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('span', attrs={'class': 'titular'}).text
                    objBody = bsObj.find('span', attrs={'class': 'cuerpo-texto'})

                elif "www.nytimes.com" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    objBody = bsObj.find('div', attrs={'class': 'story-body'})

                elif "elpais.com" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    subtitulo = bsObj.find('h2', attrs={'itemprop': 'alternativeHeadline'}).text
                    objBody = bsObj.find('div', attrs={'itemprop': 'articleBody'})

                elif "www.elmundo.es" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    objBody = bsObj.find('div', attrs={'itemprop': 'articleBody'})

                elif "www.bbc.com" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'class': 'story-body__h1'}).text
                    objBody = bsObj.find('div', attrs={'property': 'articleBody'})

                elif "www.lavozdegalicia.es" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    subtitulo = bsObj.find('h2', attrs={'itemprop': 'alternativeHeadline'}).text
                    objBody = bsObj.find('div', attrs={'itemprop': 'text'})

                elif "cruxnow.com" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'class': 'post_title'}).text
                    subtitulo = bsObj.find('p', attrs={'class': 'post_image_caption'}).text
                    objBody = bsObj.find('div', attrs={'class': 'content_box'})

                elif "www.independent.co.uk" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    objBody = bsObj.find('div', attrs={'itemprop': 'articleBody'})

                elif "www.oxfam.org" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('article', attrs={'class': 'node-8877'}).find('div', attrs={'class': 'field-name-title'}).find('h2').text
                    objBody = bsObj.find('article', attrs={'class': 'node-8877'}).find('div', attrs={'class': 'field-name-body'})

                elif "www.ft.com" in origen:
                    hayQueTratar = True
                    titulo = bsObj.find('h1', attrs={'data-trackable': 'header'}).find('span').text
                    objBody = bsObj.find('div', attrs={'data-trackable': 'article-body'})

                if hayQueTratar:
                    titulo = titulo.replace("\n", "")
                    titulo = titulo.replace("?", " _ ")
                    titulo = titulo.replace(":", " _ ")

                    f2 = open(folderDestino + "/" + titulo + ".txt", "w")

                    if subtitulo != None:
                        subtitulo = subtitulo.replace("\n", "")
                        f2.write(subtitulo + "\n")

                    if objBody != None:
                        for parrafo in objBody.findAll('p'):
                            aux = parrafo.text

                            if cad_inicio != None and cad_fin != None:

                                pos_inicio = aux.find(cad_inicio)
                                pos_fin = aux.find(cad_fin) + len(cad_fin)

                                if pos_inicio != -1 or pos_fin != -1:
                                    aux = aux[:pos_inicio] + aux[pos_fin:]

                            f2.write(aux + "\n")

                    f2.close()

def limpia_signos_puntuacion(texto):
    text_limpio = ''
    for letter in texto:
        if not letter in string.punctuation:
            text_limpio = text_limpio + letter

    return text_limpio

def limpia_stop_words(tokens, idioma):
    if idioma == 'en':
        stopWords = nltk.corpus.stopwords.words('english')
    elif idioma == 'es':
        stopWords = nltk.corpus.stopwords.words('spanish')

    return [w for w in tokens if w.lower() not in stopWords]

def extrae_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extrae_entity_names(child))
    return entity_names

def trata_entity_names(tokens):
    tagged_sentences = [nltk.pos_tag(tokens)]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
    entity_names = []
    for tree in chunked_sentences:
        entity_names.extend(extrae_entity_names(tree))

    return entity_names

def stemming(tokens, idioma):
    # Seleccionamos el steamer que deseados utilizar.
    if idioma == 'en':
        stemmer = PorterStemmer()
    else:
        stemmer = SnowballStemmer("spanish")

    stemmeds = []

    # Para cada token del texto obtenemos su raíz.
    for token in tokens:
        stemmed = stemmer.stem(token)
        stemmeds.append(stemmed)

    return stemmeds

def wordnet_value(value):
    result = ''
    # Filtramos las palabras y nos quedamos solo las que nos pueden interesar.
    # Estas son Adjetivos, Verbos, Sustantivos y Adverbios.
    if value.startswith('J'):
        return wordnet.ADJ
    elif value.startswith('V'):
        return wordnet.VERB
    elif value.startswith('N'):
        return wordnet.NOUN
    elif value.startswith('R'):
        return wordnet.ADV
    return result

def lemmatization(tokens, idioma):
    if idioma != 'en':
        return tokens

    wordnet_lemmatizer = WordNetLemmatizer()
    tokens_aux = nltk.pos_tag(tokens)
    lemmatizeds = []

    for token in tokens_aux:
        if len(token) > 0:
            pos = wordnet_value(token[1])
            # Filtramos las palabras que no nos interesan.
            if pos != '':
                lemmatizeds.append(wordnet_lemmatizer.lemmatize(str(token[0]).lower(), pos=pos))

    return lemmatizeds

if __name__ == "__main__":
    folder = "CorpusNoticiasPractica1718"
    # Empty list to hold text documents.
    texts = []

    tratamientoHTML(folder, folder + "/txt")

    listing = os.listdir(folder + "/txt")
    for file in listing:

        if file.endswith(".txt"):
            url = folder+"/txt/"+file
            f = open(url,encoding="ANSI");
            raw = f.read()
            f.close()
            t = TextBlob(raw)
            idioma = t.detect_language()
            print("File: ", file," escrito en: ", idioma)

            if idioma == 'es':
                idioma = 'en'
                raw = t.translate(to=idioma)
            raw_limpio = limpia_signos_puntuacion(raw)
            tokens = nltk.word_tokenize(raw_limpio)
            tokens_limpio = limpia_stop_words(tokens, idioma)

            #text = nltk.Text(trata_entity_names(tokens_limpio))

            #text = nltk.Text(stemming(tokens_limpio, idioma))

            #text = nltk.Text(lemmatization(tokens_limpio, idioma))

            #text = nltk.Text(stemming(lemmatization(tokens_limpio, idioma),idioma))

            text = nltk.Text(stemming(trata_entity_names(tokens_limpio), idioma))

            #text = nltk.Text(tokens_limpio)

            texts.append(text)

    print("Prepared ", len(texts), " documents...")
    print("They can be accessed using texts[0] - texts[" + str(len(texts)-1) + "]")

    distanceFunction ="cosine"
    #distanceFunction = "euclidean"
    test = cluster_texts(texts,5,distanceFunction)
    print("test: ", test)
    # Gold Standard
    reference =[0, 5, 0, 0, 0, 2, 2, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 2, 0, 2, 5]
    print("reference: ", reference)

    # Evaluation
    print("rand_score: ", adjusted_rand_score(reference,test))

