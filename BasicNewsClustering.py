import re, pprint, os, numpy
import nltk
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
    clusters = clusterer.fit_predict(vectors)

    return clusters

# Function to create a TF vector for one document. For each of
# our unique words, we have a feature which is the tf for that word
# in the current document
def TF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf(word, document))
    return word_tf

if __name__ == "__main__":
    folder = "CorpusNoticiasPractica1718"
    # Empty list to hold text documents.
    texts = []

    listing = os.listdir(folder)

    for file in listing:
        if file.endswith(".html"):
            print(file)
            f = open(folder+"/"+file)
            bsObj = BeautifulSoup(f, "html.parser")
            f.close()


            origen = bsObj.find(text=lambda text:isinstance(text, Comment))
            if "saved from url" in origen: # puedo identificar desde donde se ha descargado la página
                if "www.theguardian.com" in origen:
                    #titulo = bsObj.select('#article > div:nth-of-type(2) > div > div:nth-of-type(1) > div > header > div:nth-of-type(3) > div:nth-of-type(1) > div > h1')[0].text
                    titulo = bsObj.find('h1', attrs={'class' : 'content__headline'}).text
                    titulo = titulo.replace("\n","")

                    f2 = open(folder+"/txt/"+titulo+".txt", "w")

                    for parrafo in bsObj.find('div', attrs={'itemprop' : 'articleBody'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()

                if "www.telegraph.co.uk" in origen:
                    titulo = bsObj.find('h1', attrs={'itemprop' : 'headline name'}).text
                    titulo = titulo.replace("\n", "")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")

                    for parrafo in bsObj.find('article', attrs={'itemprop': 'articleBody'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()

                if "www.abc.es" in origen:
                    titulo = bsObj.find('span', attrs={'class': 'titular'}).text
                    titulo = titulo.replace("\n", "")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")

                    for parrafo in bsObj.find('span', attrs={'class': 'cuerpo-texto'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()

                if "www.nytimes.com" in origen:
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    titulo = titulo.replace("\n", "")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")

                    for parrafo in bsObj.find('div', attrs={'class': 'story-body'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()

                if "elpais.com" in origen:
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    titulo = titulo.replace("\n", "")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")

                    subtitulo = bsObj.find('h2', attrs={'itemprop': 'alternativeHeadline'}).text
                    subtitulo = subtitulo.replace("\n", "")
                    f2.write(subtitulo)

                    for parrafo in bsObj.find('div', attrs={'itemprop': 'articleBody'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()


                if "www.elmundo.es" in origen:
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    titulo = titulo.replace("\n", "")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")


                    for parrafo in bsObj.find('div', attrs={'itemprop': 'articleBody'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()

                if "www.bbc.com" in origen:
                    titulo = bsObj.find('h1', attrs={'class': 'story-body__h1'}).text
                    titulo = titulo.replace("\n", "")
                    titulo = titulo.replace(":", " _ ")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")

                    for parrafo in bsObj.find('div', attrs={'property': 'articleBody'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()

                if "www.lavozdegalicia.es" in origen:
                    titulo = bsObj.find('h1', attrs={'itemprop': 'headline'}).text
                    titulo = titulo.replace("\n", "")

                    f2 = open(folder + "/txt/" + titulo + ".txt", "w")

                    subtitulo = bsObj.find('h2', attrs={'itemprop': 'alternativeHeadline'}).text
                    subtitulo = subtitulo.replace("\n", "")
                    f2.write(subtitulo)

                    for parrafo in bsObj.find('div', attrs={'itemprop': 'text'}).findAll('p'):
                        f2.write(parrafo.text)

                    f2.close()
    # for file in listing:
    #     #print("File: ",file)
    #     if file.endswith(".txt"):
    #         url = folder+"/"+file
    #         f = open(url,encoding="latin-1");
    #         raw = f.read()
    #         f.close()
    #         tokens = nltk.word_tokenize(raw)
    #         text = nltk.Text(tokens)
    #         texts.append(text)
    #
    # print("Prepared ", len(texts), " documents...")
    # print("They can be accessed using texts[0] - texts[" + str(len(texts)-1) + "]")
    #
    # distanceFunction ="cosine"
    # #distanceFunction = "euclidean"
    # test = cluster_texts(texts,5,distanceFunction)
    # print("test: ", test)
    # # Gold Standard
    # reference =[0, 5, 0, 0, 0, 2, 2, 2, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 0, 2, 5]
    # print("reference: ", reference)
    #
    # # Evaluation
    # print("rand_score: ", adjusted_rand_score(reference,test))

