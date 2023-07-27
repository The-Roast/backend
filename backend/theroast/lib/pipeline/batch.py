from typing import List, Dict, Any
import math
from collections import defaultdict
import numpy as np

from hdbscan import HDBSCAN
from umap import UMAP
from sklearn.metrics.pairwise import cosine_similarity
from cohere.client import Reranking

from ..models import COHERE, ST_ENCODER


def _parse_clusters(labels: List[int], articles: List[str]) -> Dict[int, List[str]]:
    """
    Parse clusters from labels and articles.

    :param labels: List of labels
    :param articles: List of articles
    :return: A dictionary of clusters
    """
    if len(labels) != len(articles):
        raise ValueError("Labels and Articles should have same length")
    clusters = defaultdict(list)
    for label, article in zip(labels, articles):
        clusters[label].append(article)
    clusters.pop(-1, None)
    return clusters

def _parse_rankings(rankings: Reranking) -> Dict[str, float]:
    """
    Parse rankings from a list.

    :param rankings: List of rankings
    :return: A dictionary of rankings
    """
    output = {}
    for ranking in rankings:
        if 'text' in ranking.document and 'relevance_score' in ranking:
            output[ranking.document['text']] = ranking.relevance_score
            continue
        raise KeyError("Key not found in ranking or document")
    return output


def _cluster(
        embeddings: Any,
        n_neighbors: int = 15,
        n_components: int = 5,
        min_cluster_size: int = 3,
        random_state: int = 42
    ) -> HDBSCAN:
    """
    Cluster the embeddings.

    :param embeddings: Article embeddings
    :param n_neighbors: Number of neighbors to consider
    :param n_components: Number of components to keep
    :param min_cluster_size: Minimum cluster size
    :param random_state: Random state for reproducibility
    :return: Clusters
    """
    _embeddings = UMAP(n_neighbors=n_neighbors, n_components=n_components, metric='cosine', random_state=random_state).fit_transform(embeddings)
    return HDBSCAN(min_cluster_size=min_cluster_size).fit(_embeddings)


def _rank(articles: List[str], query: str) -> Reranking:
    """
    Rank the clusters based on their average score.

    :param clusters: Dictionary of clusters
    :param rankings: Dictionary of rankings
    :return: List of tuples containing articles and their average score
    """
    return COHERE.rerank(query=query, model="rerank-english-v2.0", documents=articles)


def _rank_clusters(clusters: Dict[int, List[str]], rankings: Dict[str, float]) -> List[tuple]:
    """
    Rank the clusters based on their average score.

    :param clusters: Dictionary of clusters
    :param rankings: Dictionary of rankings
    :return: List of tuples containing articles and their average score
    """
    output = []
    for cluster, articles in clusters.items():
        article_scores = [(article, rankings.get(article, 0)) for article in articles]
        article_scores.sort(key=lambda x: x[1], reverse=True)
        average_score = np.mean([score for _, score in article_scores])
        output.append(([article for article, _ in article_scores], average_score))
    return sorted(output, key=lambda x: x[1], reverse=True)


def _extract(
        cluster_articles: Dict[int, List[str]],
        article_embeddings: Dict[str, Any],
        proportion: float,
        floor: float = 0.75
    ) -> Dict[int, List[str]]:
    """
    Extract the articles that are most relevant based on cosine similarity.

    :param cluster_articles: Dictionary containing cluster id and corresponding articles
    :param article_embeddings: Dictionary containing article and its corresponding embedding
    :param proportion: Proportion of articles to retain
    :param floor: Threshold for cosine similarity
    :return: Dictionary of articles after extraction
    """
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


def batch(
        articles: List[str],
        query: str,
        target: int = 20,
        threshold: float = 0.0
    ) -> Dict[int, List[str]]:
    """
    Batch process the articles to obtain the most relevant articles based on a query.

    :param articles: List of articles
    :param query: Query for ranking
    :param target: Target number of articles to retain
    :param threshold: Threshold for relevance score
    :return: Dictionary of final selected articles
    """
    embeddings = ST_ENCODER.encode(articles)
    article_embedding = {article: embeddings[i] for i, article in enumerate(articles)}
    
    clusters = _cluster(embeddings).labels_
    cluster_articles = _parse_clusters(clusters, articles)
    
    rankings = _rank(articles, query)
    article_ranking = _parse_rankings(rankings)
    
    clusters_by_rank = _rank_clusters(cluster_articles, article_ranking)
    clusters_by_rank = [cluster for cluster in clusters_by_rank if cluster[1] > threshold]
    
    extraction_proportion = target / sum(len(cluster[0]) for cluster in clusters_by_rank)
    return _extract(cluster_articles, article_embedding, proportion=extraction_proportion)