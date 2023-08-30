import os
import faiss
import pickle
import numpy as np
from base.log import logger
from base.config import settings

# much more threads will cause segment error
faiss.omp_set_num_threads(settings.FAISS_THREADS)


class IndexManager:
    def __init__(self, index_dir):
        self.index_path = os.path.join(index_dir, "vector.index")
        self.embedding_size = settings.EMBEDDING_SIZE
        self.index_method = settings.INDEX_METHOD
        self.top_k = settings.TOP_K
        self.index = None
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

    def _save_index(self):
        if self.index is None:
            logger.error("index is None please create index firstly")
            return
        faiss.write_index(self.index, self.index_path)

    @staticmethod
    def _get_features_ids(libs: dict):
        features = None
        ids = []
        for id_ in libs.keys():
            ids.append(id_)
            feature: np.ndarray = libs[id_]["feature"]
            feature = feature.reshape((-1, feature.size))
            features = feature if features is None else np.concatenate([features, feature], axis=0)
        return features, np.array(ids).astype("int64")

    def build_index(self, libs: dict):
        if not libs:
            logger.warning("facelib cache is empty")
            return
        if self.index_method.lower() not in ['hnsw32', 'ivf', 'flat']:
            logger.error("The index method Only support: HNSW32, IVF, Flat")
            return
        features, ids = self._get_features_ids(libs)
        # generate index
        if self.index_method == "IVF":
            self.index_method = self.index_method + str(
                min(max(int(features.shape[0] // 32), 2), 65536)) + ",Flat"
        index = faiss.index_factory(self.embedding_size, self.index_method,
                                    faiss.METRIC_INNER_PRODUCT)
        self.index = faiss.IndexIDMap2(index)
        self.index.train(features)
        self.index.add_with_ids(features, ids)
        self._save_index()

    def search_result(self, feature):
        if not isinstance(feature, np.ndarray):
            feature = np.array(feature)
        dims = len(feature.shape)
        if dims != 2:
            logger.warning("feature dim must be 2, will force reshape")
        feature = feature.reshape((-1, self.embedding_size))
        if self.index is None:
            logger.error("index is None please create index firstly")
            return
        distance, index = self.index.search(feature, self.top_k)
        return distance, index


if __name__ == '__main__':
    st = IndexManager()
    face_libs = pickle.load(open("facelib/facelib.pkl", "rb"))
    st.build_index(face_libs)
