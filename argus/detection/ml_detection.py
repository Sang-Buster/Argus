"""
Machine Learning-based anomaly detection using Node2Vec + Isolation Forest.

Combines graph embeddings with ML anomaly detection for improved accuracy.
"""

import time
from typing import Optional

import networkx as nx
import numpy as np
from node2vec import Node2Vec
from sklearn.ensemble import IsolationForest

from argus.detection import AnomalyDetector
from argus.evaluation import DetectionResult
from argus.utils.logging_config import get_logger

logger = get_logger(__name__)


class Node2VecDetector(AnomalyDetector):
    """
    ML-based detection using Node2Vec embeddings + Isolation Forest.

    Generates graph embeddings using random walks, then trains an
    isolation forest to identify anomalous nodes in embedding space.

    This typically provides better accuracy than pure graph metrics
    but at higher computational cost.
    """

    def __init__(
        self,
        name: str = "node2vec",
        embedding_dim: int = 128,
        walk_length: int = 30,
        num_walks: int = 200,
        p: float = 1.0,
        q: float = 1.0,
        contamination: float = 0.1,
    ):
        """
        Initialize Node2Vec detector.

        Args:
            name: Detector identifier
            embedding_dim: Dimension of embedding vectors
            walk_length: Length of each random walk
            num_walks: Number of walks per node
            p: Return parameter (controls walk strategy)
            q: In-out parameter (controls walk strategy)
            contamination: Expected fraction of anomalies in data
        """
        super().__init__(name)
        self.embedding_dim = embedding_dim
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.p = p
        self.q = q
        self.contamination = contamination

        # ML model
        self.isolation_forest: Optional[IsolationForest] = None
        self.node2vec_model = None
        self.baseline_embeddings: dict[str, np.ndarray] = {}

    def train(self, clean_graphs: list[nx.Graph]) -> None:
        """
        Train Node2Vec embeddings and Isolation Forest.

        Args:
            clean_graphs: Time series of graphs without attacks

        Steps:
            1. Generate random walks on clean graphs
            2. Train Word2Vec to learn embeddings
            3. Fit Isolation Forest on clean embeddings
        """
        self.baseline_graphs = clean_graphs

        if not clean_graphs:
            logger.warning("No clean graphs provided for training")
            return

        # Use the most recent graph (or merge multiple graphs)
        training_graph = clean_graphs[-1].copy()

        if len(training_graph.nodes()) == 0:
            logger.warning("Training graph is empty")
            return

        logger.info(
            f"Training Node2Vec on graph with {training_graph.number_of_nodes()} nodes..."
        )

        try:
            # Generate Node2Vec embeddings
            node2vec = Node2Vec(
                training_graph,
                dimensions=self.embedding_dim,
                walk_length=self.walk_length,
                num_walks=self.num_walks,
                p=self.p,
                q=self.q,
                workers=1,  # Single worker for reproducibility
                quiet=True,
            )

            # Train Word2Vec model
            self.node2vec_model = node2vec.fit(window=10, min_count=1, batch_words=4)

            # Generate embeddings for all nodes
            embeddings_list = []
            for node in training_graph.nodes():
                try:
                    embedding = self.node2vec_model.wv[str(node)]
                    self.baseline_embeddings[str(node)] = embedding
                    embeddings_list.append(embedding)
                except KeyError:
                    logger.warning(f"No embedding for node {node}")

            if not embeddings_list:
                logger.error("No embeddings generated")
                return

            # Train Isolation Forest on clean embeddings
            embeddings_array = np.array(embeddings_list)
            self.isolation_forest = IsolationForest(
                n_estimators=100,
                contamination=self.contamination,
                random_state=42,
                n_jobs=1,
            )
            self.isolation_forest.fit(embeddings_array)

            logger.info(
                f"Node2Vec detector trained on {len(embeddings_list)} node embeddings"
            )

        except Exception as e:
            logger.error(f"Error training Node2Vec: {e}")
            self.isolation_forest = None

    def detect(self, graph: nx.Graph) -> DetectionResult:
        """
        Detect anomalies in embedding space.

        Args:
            graph: Current swarm graph to analyze

        Returns:
            DetectionResult with flagged UAVs

        Steps:
            1. Generate embeddings for current graph
            2. Predict anomaly scores with Isolation Forest
            3. Threshold scores to flag anomalous nodes
        """
        start_time = time.time()

        confidence_scores = {}
        anomalous_uav_ids = set()
        ground_truth = {}

        if len(graph.nodes()) == 0 or self.isolation_forest is None:
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={},
                ground_truth={},
                detection_time=detection_time,
            )

        try:
            # Generate Node2Vec embeddings for current graph
            node2vec = Node2Vec(
                graph,
                dimensions=self.embedding_dim,
                walk_length=self.walk_length,
                num_walks=self.num_walks,
                p=self.p,
                q=self.q,
                workers=1,
                quiet=True,
            )

            current_model = node2vec.fit(window=10, min_count=1, batch_words=4)

            # Get embeddings for all nodes
            embeddings_list = []
            node_list = []

            for node in graph.nodes():
                try:
                    embedding = current_model.wv[str(node)]
                    embeddings_list.append(embedding)
                    node_list.append(node)
                except KeyError:
                    logger.warning(f"No embedding for node {node}")

            if not embeddings_list:
                logger.warning("No embeddings generated for current graph")
                detection_time = time.time() - start_time
                return DetectionResult(
                    detector_name=self.name,
                    timestamp=time.time(),
                    anomalous_uav_ids=set(),
                    confidence_scores={},
                    ground_truth={},
                    detection_time=detection_time,
                )

            # Predict anomaly scores
            embeddings_array = np.array(embeddings_list)
            anomaly_scores = self.isolation_forest.decision_function(embeddings_array)
            predictions = self.isolation_forest.predict(embeddings_array)

            # Normalize scores to [0, 1] range (lower = more anomalous)
            min_score = anomaly_scores.min()
            max_score = anomaly_scores.max()
            score_range = max_score - min_score

            for node, score, pred in zip(node_list, anomaly_scores, predictions):
                # Convert to confidence score (higher = more anomalous)
                if score_range > 0:
                    normalized_score = 1.0 - (score - min_score) / score_range
                else:
                    normalized_score = 0.5

                confidence_scores[node] = float(normalized_score)

                # Flag if predicted as anomaly (-1)
                if pred == -1:
                    anomalous_uav_ids.add(node)

            # Get ground truth
            for node in graph.nodes():
                node_data = graph.nodes[node]
                if "uav" in node_data:
                    uav = node_data["uav"]
                    ground_truth[node] = uav.is_legitimate
                else:
                    ground_truth[node] = True

            detection_time = time.time() - start_time

            logger.debug(
                f"Node2Vec detection: {len(anomalous_uav_ids)} anomalies detected"
            )

            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=anomalous_uav_ids,
                confidence_scores=confidence_scores,
                ground_truth=ground_truth,
                detection_time=detection_time,
            )

        except Exception as e:
            logger.error(f"Error in Node2Vec detection: {e}")
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={},
                ground_truth={},
                detection_time=detection_time,
            )
