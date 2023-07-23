import math
from collections import defaultdict

import hdbscan
import umap
from sklearn.metrics.pairwise import cosine_similarity

from ..models import COHERE, ST_ENCODER

def cluster(embeddings, n_neighbors=5, n_components=50, min_cluster_size=2, random_state=None):
    _embeddings = umap.UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components, 
        metric='cosine', 
        random_state=random_state
    ).fit_transform(embeddings)
    clusters = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric='euclidean', 
        cluster_selection_method='eom'
    ).fit(_embeddings)
    return clusters

def parse_clusters(labels, articles):
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[label].append(articles[i])
    return clusters

def parse_rankings(rankings):
    output = {ranking.document['text']: ranking.relevance_score for ranking in rankings}
    return output

def rerank(articles, q):
    rankings = COHERE.rerank(query=q, model="rerank-english-v2.0", documents=articles)
    return rankings

def rank_clusters(clusters, rankings):
    output = []
    for cluster, articles in clusters.items():
        vbr = [(article, rankings[article]) for article in articles]
        vbr.sort(key=lambda x: x[1], reverse=True)
        average_score = sum(score for _, score in vbr) / len(vbr)
        output.append(([article for article, _ in vbr], average_score))
    output.sort(key=lambda x: x[1], reverse=True)
    return output

def filter_by_rank(clusters, threshold=0):
    return [cluster for cluster in clusters if cluster[1] > threshold]

def extract(cluster_articles, article_embeddings, proportion, floor=0.75):
    output = {}
    for cluster, articles in cluster_articles.items():
        _extracted_articles = []
        for article in articles:
            if all(cosine_similarity([article_embeddings[article]], 
                                      [article_embeddings[already_extracted]])[0][0] <= floor 
                   for already_extracted in _extracted_articles):
                _extracted_articles.append(article)
        if len(_extracted_articles) > len(articles) * proportion:
            _extracted_articles = _extracted_articles[:math.ceil(len(articles) * proportion)]
        output[cluster] = _extracted_articles
    return output

def extract_and_cluster(articles, q, target=20):
    embeddings = ST_ENCODER.encode(articles)    
    article_embedding = {article: embeddings[i] for i, article in enumerate(articles)}
    clusters = cluster(
        embeddings, 
        n_neighbors=15, 
        n_components=5,
        min_cluster_size=3, 
        random_state=42
    )
    cluster_articles = parse_clusters(clusters.labels_, articles)
    if -1 in cluster_articles.keys():
        del cluster_articles[-1]
    rankings = rerank(articles, q)
    article_ranking = parse_rankings(rankings)
    cbr = rank_clusters(cluster_articles, article_ranking)
    cbr = filter_by_rank(cbr)
    extraction_proportion = target / sum(len(c[0]) for c in cbr)
    output = extract(cluster_articles, article_embedding, proportion=extraction_proportion)
    return output