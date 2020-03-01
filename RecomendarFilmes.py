# -*- coding: utf-8 -*-
"""filmes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19K7mC53xVHnFGfs5qPdIiGK0PknlpWXe
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

uri_filmes = 'https://raw.githubusercontent.com/alura-cursos/machine-learning-algoritmos-nao-supervisionados/master/movies.csv'

filmes = pd.read_csv(uri_filmes)
filmes.columns = ['filme_id', 'titulo', 'generos']
filmes.head()

generos = filmes.generos.str.get_dummies()
generos.head()

dados_dos_filmes = pd.concat([filmes, generos], axis=1)
dados_dos_filmes.head()

scaler = StandardScaler()
generos_escalados = scaler.fit_transform(generos)
generos_escalados.shape

modelo = KMeans(n_clusters=3)

modelo.fit(generos_escalados)

#print(f'Grupos: {modelo.labels_}')

"""https://www.naftaliharris.com/blog/visualizing-k-means-clustering/"""

print(generos.columns)
print(modelo.cluster_centers_)

grupos = pd.DataFrame(modelo.cluster_centers_,
             columns = generos.columns)

grupos

grupos.transpose().plot.bar(subplots=True,
                figsize = (25,25),
                sharex = False)

grupo = 0
filtro = (modelo.labels_ == grupo)
dados_dos_filmes[filtro].sample(10)

tsne = TSNE()

visualizacao = tsne.fit_transform(generos_escalados)
visualizacao

sns.set(rc={'figure.figsize': (13, 13)})

sns.scatterplot(x=visualizacao[:,0],
                y=visualizacao[:,1],
                hue = modelo.labels_,
                palette = sns.color_palette('Set1', 3))

modelo = KMeans(n_clusters = 20)

modelo.fit(generos_escalados)

grupos = pd.DataFrame(modelo.cluster_centers_,
             columns = generos.columns)

grupos.transpose().plot.bar(subplots=True,
                figsize = (25,50),
                sharex = False,
                rot = 0)

grupo = 15
filtro = (modelo.labels_ == grupo)
dados_dos_filmes[filtro].sample(10)

def kmeans(numero_de_clusters, generos):
  modelo = KMeans(n_clusters = numero_de_clusters)
  modelo.fit(generos)
  return [numero_de_clusters, modelo.inertia_]

kmeans(20, generos_escalados)

kmeans(3, generos_escalados)

resultado = [kmeans(numero_de_grupos, generos_escalados) for numero_de_grupos in range(1,41)]
resultado

resultado = pd.DataFrame(resultado,
             columns=['grupos', 'inertia'])

resultado

resultado.inertia.plot(xticks=resultado.grupos)

modelo = KMeans(n_clusters=17)
modelo.fit(generos_escalados)

grupos = pd.DataFrame(modelo.cluster_centers_,
             columns = generos.columns)

grupos.transpose().plot.bar(subplots=True,
                figsize = (25,50),
                sharex = False,
                rot = 0)

"""O agrupamento que fizemos com o KMeans é chamado de "agrupamento particionado", no qual o algoritmo divide nossos dados em grupos específicos. Mas também existem outros tipos de agrupamentos, por exemplo o agrupamento hierárquico, que tenta definir uma hierarquia entre os dados."""

modelo = AgglomerativeClustering(n_clusters=17)
grupos = modelo.fit_predict(generos_escalados)
grupos

tsne = TSNE()
visualizacao = tsne.fit_transform(generos_escalados)
visualizacao

sns.scatterplot(x=visualizacao[:,0],
                y=visualizacao[:,1],
                hue = grupos,
                palette = sns.color_palette('Set1', 17))

#"""O nome do gráfico a ser gerado é "dendrograma""""

modelo = KMeans(n_clusters=17)
modelo.fit(generos_escalados)

grupos = pd.DataFrame(modelo.cluster_centers_,
             columns = generos.columns)

grupos.transpose().plot.bar(subplots=True,
                figsize = (25,50),
                sharex = False,
                rot = 0)

matriz_de_distancia = linkage(grupos)
matriz_de_distancia

dendograma = dendrogram(matriz_de_distancia)