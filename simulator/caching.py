import os
import shutil
from pathlib import Path
import open3d as o3d
from .body import Body
from copy import deepcopy
from collections import defaultdict
from libmesh import ply_to_obj, obj_to_urdf
from .client import BulletClient

def create_cache_folder(cache_path):
    cache_path = Path(cache_path)
    if cache_path.is_dir():
        shutil.rmtree(cache_path)
        os.makedirs(cache_path)
    else:
        os.makedirs(cache_path)
    return cache_path

def create_urdf_folder():
    pass


class BodyCache:
    def __init__(self, client_id):
        # self.urdf_ds = urdf_ds
        self.client = BulletClient(client_id)
        self.cache = defaultdict(list)
        self.away_transform = (0, 0, 1000), (0, 0, 0, 1)

    def _load_body(self, obj_info):
        '''
        obj_info = {
            'label':'obj_000013',
            'urdf_path': '',
            'scale':0.001,
        }
        '''
        body = Body.load(obj_info['urdf_path'],
                         scale=obj_info['scale'],
                         client_id=self.client.client_id)
        body.pose = self.away_transform
        self.cache[obj_info['label']].append(body)
        return body

    def hide_bodies(self):
        n = 0
        for body_list in self.cache.values():
            for body in body_list:
                pos = (1000, 1000, 1000 + n * 10)
                orn = (0, 0, 0, 1)
                body.pose = pos, orn
                n += 1

    def get_bodies(self, obj_infos):
        self.hide_bodies()

        # cache folder
        renderer_dir = os.path.dirname(os.path.dirname(__file__))
        cache_path = os.path.join(renderer_dir, 'cache')
        create_cache_folder(cache_path)

        gb_label = defaultdict(lambda: 0)
        for obj in obj_infos:
            if 'urdf_path' not in obj:
                # urdf generation
                ply_path = os.path.join(cache_path, obj['label']+'.ply')
                obj_path = os.path.join(cache_path, obj['label']+'.obj')
                urdf_path = os.path.join(cache_path, obj['label']+'.urdf')
                o3d.io.write_triangle_mesh(ply_path, obj['mesh'])
                ply_to_obj(ply_path=ply_path, obj_path=obj_path)
                obj_to_urdf(obj_path=obj_path, urdf_path=urdf_path)
                obj['urdf_path'] = urdf_path

            gb_label[obj['label']] += 1

        for label, obj_info in zip(gb_label.keys(), obj_infos):
            n_missing = gb_label[label] - len(self.cache[label])
            for n in range(n_missing):
                self._load_body(obj_info)

        remaining = deepcopy(dict(self.cache))
        bodies = [remaining[obj['label']].pop(0) for obj in obj_infos]
        return bodies

    def __len__(self):
        return sum([len(bodies) for bodies in self.cache.values()])
