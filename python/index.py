from base.config import settings
import pickle
import cv2
import os
import faiss
from face import FACE_IMAGE_DIR


class ShiTuIndexManager:
    def __init__(self, config):
        self.root_path = settings.BASE_DIR
        self.image_list_path = os.path.join(FACE_IMAGE_DIR, "image_list.txt")
        self.image_dir = os.path.join(FACE_IMAGE_DIR, "images")
        self.index_path = os.path.join(FACE_IMAGE_DIR, "index", "vector.index")
        self.id_map_path = os.path.join(FACE_IMAGE_DIR, "index", "id_map.pkl")
        self.features_path = os.path.join(FACE_IMAGE_DIR, "features.pkl")
        self.index = None
        self.id_map = None
        self.features = None
        self.config = config

    @staticmethod
    def _load_pickle(path):
        if os.path.exists(path):
            return pickle.load(open(path, 'rb'))
        else:
            return None

    @staticmethod
    def _save_pickle(path, data):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as fd:
            pickle.dump(data, fd)

    def _load_index(self):
        self.index = faiss.read_index(self.index_path)
        self.id_map = self._load_pickle(self.id_map_path)
        self.features = self._load_pickle(self.features_path)

    def _save_index(self, index, id_map, features):
        faiss.write_index(index, os.path.join(self.root_path, self.index_path))
        self._save_pickle(
            os.path.join(self.root_path, self.id_map_path), id_map)
        self._save_pickle(
            os.path.join(self.root_path, self.features_path), features)

    def _update_path(self, root_path, image_list_path=None):
        if root_path == self.root_path:
            pass
        else:
            self.root_path = root_path
            if not os.path.exists(os.path.join(root_path, "index")):
                os.mkdir(os.path.join(root_path, "index"))
            if image_list_path is not None:
                self.image_list_path = image_list_path

    def _cal_featrue(self, image_list):
        batch_images = []
        featrures = None
        cnt = 0
        for idx, image_path in enumerate(image_list):
            image = cv2.imread(image_path)
            if image is None:
                return "{} is broken or not exist. Stop"
            else:
                image = image[:, :, ::-1]
                batch_images.append(image)
                cnt += 1
            if cnt % self.config["Global"]["batch_size"] == 0 or (
                    idx + 1) == len(image_list):
                if len(batch_images) == 0:
                    continue
                batch_results = self.predictor.predict(batch_images)
                featrures = None
                batch_images = []
        return featrures

    def _split_datafile(self, data_file, image_root):
        '''
        data_file: image path and info, which can be splitted by spacer
        image_root: image path root
        delimiter: delimiter
        '''
        gallery_images = []
        gallery_docs = []
        gallery_ids = []
        with open(data_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for _, ori_line in enumerate(lines):
                line = ori_line.strip().split()
                text_num = len(line)
                assert text_num >= 2, f"line({ori_line}) must be splitted into at least 2 parts, but got {text_num}"
                image_file = os.path.join(image_root, line[0])

                gallery_images.append(image_file)
                gallery_docs.append(ori_line.strip())
                gallery_ids.append(os.path.basename(line[0]).split(".")[0])

        return gallery_images, gallery_docs, gallery_ids

    def create_index(self,
                     image_list: str,
                     index_method: str = "HNSW32",
                     image_root: str = None):
        if not os.path.exists(image_list):
            return "{} is not exist".format(image_list)
        if index_method.lower() not in ['hnsw32', 'ivf', 'flat']:
            return "The index method Only support: HNSW32, IVF, Flat"
        self._update_path(os.path.dirname(image_list), image_list)

        # get image_paths
        image_root = image_root if image_root is not None else self.root_path
        gallery_images, gallery_docs, image_ids = self._split_datafile(
            image_list, image_root)

        # gernerate index
        if index_method == "IVF":
            index_method = index_method + str(
                min(max(int(len(gallery_images) // 32), 2), 65536)) + ",Flat"
        index = faiss.index_factory(
            self.config["IndexProcess"]["embedding_size"], index_method,
            faiss.METRIC_INNER_PRODUCT)
        self.index = faiss.IndexIDMap2(index)
        features = self._cal_featrue(gallery_images)
        self.index.train(features)
        index_ids = np.arange(0, len(gallery_images)).astype(np.int64)
        self.index.add_with_ids(features, index_ids)

        self.id_map = dict()
        for i, d in zip(list(index_ids), gallery_docs):
            self.id_map[i] = d

        self.features = {
            "features": features,
            "index_method": index_method,
            "image_ids": image_ids,
            "index_ids": index_ids.tolist()
        }
        self._save_index(self.index, self.id_map, self.features)

    def open_index(self, root_path: str, image_list_path: str) -> str:
        self._update_path(root_path)
        _, _, image_ids = self._split_datafile(image_list_path, root_path)
        if os.path.exists(os.path.join(self.root_path, self.index_path)) and \
                os.path.exists(os.path.join(self.root_path, self.id_map_path)) and \
                os.path.exists(os.path.join(self.root_path, self.features_path)):
            self._update_path(root_path)
            self._load_index()
            if operator.eq(set(image_ids), set(self.features['image_ids'])):
                return ""
            else:
                return "The image list is different from index, Please update index"
        else:
            return "File not exist: features.pkl, vector.index, id_map.pkl"

    def update_index(self, image_list: str, image_root: str = None) -> str:
        if self.index and self.id_map and self.features:
            image_paths, image_docs, image_ids = self._split_datafile(
                image_list, image_root
                if image_root is not None else self.root_path)

            # for add image
            add_ids = list(
                set(image_ids).difference(set(self.features["image_ids"])))
            add_indexes = [i for i, x in enumerate(image_ids) if x in add_ids]
            add_image_paths = [image_paths[i] for i in add_indexes]
            add_image_docs = [image_docs[i] for i in add_indexes]
            add_image_ids = [image_ids[i] for i in add_indexes]
            self._add_index(add_image_paths, add_image_docs, add_image_ids)

            # delete images
            delete_ids = list(
                set(self.features["image_ids"]).difference(set(image_ids)))
            self._delete_index(delete_ids)
            self._save_index(self.index, self.id_map, self.features)
            return ""
        else:
            return "Failed. Please create or open index first"

    def _add_index(self, image_list: list, image_docs: list, image_ids: list):
        if len(image_ids) == 0:
            return
        featrures = self._cal_featrue(image_list)
        index_ids = (
                np.arange(0, len(image_list)) + max(self.id_map.keys()) + 1
        ).astype(np.int64)
        self.index.add_with_ids(featrures, index_ids)

        for i, d in zip(index_ids, image_docs):
            self.id_map[i] = d

        self.features['features'] = np.concatenate(
            [self.features['features'], featrures], axis=0)
        self.features['image_ids'].extend(image_ids)
        self.features['index_ids'].extend(index_ids.tolist())

    def _delete_index(self, image_ids: list):
        if len(image_ids) == 0:
            return
        indexes = [
            i for i, x in enumerate(self.features['image_ids'])
            if x in image_ids
        ]
        self.features["features"] = np.delete(
            self.features["features"], indexes, axis=0)
        self.features["image_ids"] = np.delete(
            np.asarray(self.features["image_ids"]), indexes, axis=0).tolist()
        index_ids = np.delete(
            np.asarray(self.features["index_ids"]), indexes, axis=0).tolist()
        id_map_values = [self.id_map[i] for i in index_ids]
        self.index.reset()
        ids = np.arange(0, len(id_map_values)).astype(np.int64)
        self.index.add_with_ids(self.features['features'], ids)
        self.id_map.clear()
        for i, d in zip(ids, id_map_values):
            self.id_map[i] = d
        self.features["index_ids"] =
