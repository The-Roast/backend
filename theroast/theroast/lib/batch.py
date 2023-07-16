from collections import defaultdict
import math
import umap
import hdbscan
from sklearn.metrics.pairwise import cosine_similarity
from .extensions import CO, ST

def cluster(embeddings, n_neighbors = 5, n_components = 50, min_cluster_size = 2, random_state = None):

    _embeddings = umap.UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components, 
        metric='cosine', 
        random_state=random_state).fit_transform(embeddings)
    clusters = hdbscan.HDBSCAN(
        min_cluster_size = min_cluster_size,
        metric='euclidean', 
        cluster_selection_method='eom').fit(_embeddings)

    return clusters


def parse_clusters(labels, articles):

    clusters = defaultdict(list)
    for i, k in enumerate(labels):
        clusters[k].append(articles[i])
    
    return clusters

def parse_rankings(rankings):

    output = {}
    for i, r in enumerate(rankings):
        output[r.document['text']] = r.relevance_score
    
    return output

def rerank(articles, q):

    rankings = CO.rerank(query = q, model = "rerank-english-v2.0", documents = articles)

    return rankings

def rank_clusters(clusters, rankings):
    
    output = []
    for k, v in clusters.items():
        vbr = [(a, rankings[a]) for a in v]
        vbr.sort(key = lambda x: x[1], reverse = True)
        total = sum([n for _, n in vbr]) / len(vbr)
        output.append(([a for a, _ in vbr], total))
    output.sort(key = lambda x: x[1], reverse = True)

    return output

def filter_by_rank(clusters, threshold = 0):

    return [c for c in clusters if c[1] > threshold]

def extract(clusters, articles, proportion, floor = 0.75):

    output = {}
    for k, v in clusters.items():
        _extract = []
        for a in v:
            unique = True
            for ea in _extract:
                if cosine_similarity([articles[a]], [articles[ea]]) > floor:
                    unique = False
                    break
            if unique: _extract.append(a)
        if len(_extract) > len(v) * proportion:
            _extract = _extract[0: math.ceil(len(v) * proportion)]
        output[k] = _extract
    
    return output

def extract_and_cluster(articles, q, target = 20):

    embeddings = ST.encode(articles)    
    article__embedding = {a: embeddings[i] for i, a in enumerate(articles)}
    
    clusters = cluster(embeddings, n_neighbors = 15, n_components = 50, min_cluster_size = 3, random_state = 42)
    cluster__articles = parse_clusters(clusters.labels_, articles)    
    if -1 in cluster__articles.keys():
        del cluster__articles[-1]

    rankings = rerank(articles, q)
    article__ranking = parse_rankings(rankings)

    cbr = rank_clusters(cluster__articles, article__ranking)
    cbr = filter_by_rank(cbr)

    EXTRACTION_PROPORTION = target / sum([len(c[0]) for c in cbr])

    output = extract(cluster__articles, article__embedding, proportion = EXTRACTION_PROPORTION)

    return output