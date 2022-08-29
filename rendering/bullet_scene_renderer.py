import numpy as np
import pybullet as pb

from simulator.base_scene import BaseScene
from simulator.caching import BodyCache
from simulator.camera import Camera


class BulletSceneRenderer(BaseScene):
    def __init__(self,
                background_color=(0, 0, 0),
                gpu_renderer=True,
                gui=False,
                ):

        self.connect(gpu_renderer=gpu_renderer, gui=gui)
        self.body_cache = BodyCache(self.client_id)
        self.background_color = background_color
    
    def setup_scene(self, obj_infos):
        bodies = self.body_cache.get_bodies(obj_infos)
        for (obj_info, body) in zip(obj_infos, bodies):
            TWO = obj_info['TWO']
            body.pose = TWO
            q = obj_info.get('joints', None)
            if q is not None:
                body.q = q
            color = obj_info.get('color', None)
            if color is not None:
                pb.changeVisualShape(body.body_id, -1, physicsClientId=0, rgbaColor=color)
        return bodies
    
    def render_images(self, cam_infos, render_depth=False, render_mask=True):
        cam_obs = []
        for cam_info in cam_infos:
            K = cam_info['K']
            TWC = cam_info['TWC']
            resolution = cam_info['resolution']
            cam = Camera(resolution=resolution, client_id=self.client_id)
            cam.set_intrinsic_K(K)
            cam.set_extrinsic_T(TWC)
            cam_obs_ = cam.get_state()
            if self.background_color is not None:
                im = cam_obs_['rgb']
                mask = cam_obs_['mask']
                im[np.logical_or(mask < 0, mask == 255)] = self.background_color
                if render_depth:
                    depth = cam_obs_['depth']
                    near, far = cam_obs_['near'], cam_obs_['far']
                    z_n = 2 * depth - 1
                    z_e = 2 * near * far / (far + near - z_n * (far - near))
                    z_e[np.logical_or(mask < 0, mask == 255)] = 0.
                    cam_obs_['depth'] = z_e
            cam_obs.append(cam_obs_)
        return cam_obs

    def render_scene(self, obj_infos, cam_infos, render_depth=False, render_mask=True):
        self.setup_scene(obj_infos)
        # NOTE: Mask is always rendered, flag is not used.
        cam_obs = self.render_images(cam_infos, render_depth=render_depth, render_mask=render_mask)
        return cam_obs