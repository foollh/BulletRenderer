import os
import argparse
from mmcv import Config
import numpy as np
import transforms3d
import open3d as o3d

from libmesh import ply_to_obj, obj_to_urdf
from rendering.bullet_scene_renderer import BulletSceneRenderer
from matplotlib import pyplot as plt

def get_parser():
    parser = argparse.ArgumentParser(
        description="Render Mesh")

    parser.add_argument("--config",
                        type=str,
                        default="configs/single_obj.py",
                        help="path to mesh file")
    parser.add_argument("--use_gpu",
                        type=bool,
                        default=False,
                        help="whether use GPU to render")
    args_cfg = parser.parse_args()

    return args_cfg

def set_cam_info(cfg):
    # camera information set
    resolution = cfg.resolution
    fx, fy = cfg.fx_fy
    cx, cy = cfg.cx_cy
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    ai, aj, ak = np.pi*(cfg.angle[0])/180, np.pi*(cfg.angle[1])/180, np.pi*(cfg.angle[2])/180
    TWC = transforms3d.affines.compose(
        T=cfg.trans,
        R=transforms3d.euler.euler2mat(ai, aj, ak, axes='sxyz'),
        Z=np.ones(3)
    )

    cam = dict(
        resolution=resolution,
        K=K,
        TWC=TWC  # camera pose in world coordinate
    )
    return cam

def set_mesh_info(cfg):
    # object information set
    if 'urdf_path' not in cfg:
        mesh_folder = os.path.dirname(cfg.mesh_path)
        mesh_name, mesh_type = os.path.splitext(os.path.basename(cfg.mesh_path))
        urdf_path = os.path.join(mesh_folder, mesh_name + '.urdf')
        # generate urdf file
        if mesh_type == '.obj':
            obj_to_urdf(obj_path=cfg.mesh_path, urdf_path=urdf_path)
        # elif mesh_type == '.ply':
        #     obj_path = os.path.join(mesh_folder, mesh_name + '.obj')
        #     ply_to_obj(ply_path=cfg.mesh_path, obj_path=obj_path)
        #     obj_to_urdf(obj_path=obj_path, urdf_path=urdf_path)
        else:
            raise RuntimeError('The {} type of mesh is not support now!'.format(mesh_type))
    else:
        mesh_folder = os.path.dirname(cfg.urdf_path)
        mesh_name, mesh_type = os.path.splitext(os.path.basename(cfg.urdf_path))
        urdf_path = cfg.urdf_path

    ai, aj, ak = np.pi*(cfg.angle[0])/180, np.pi*(cfg.angle[1])/180, np.pi*(cfg.angle[2])/180
    TWO = transforms3d.affines.compose(
        T=cfg.trans,
        R=transforms3d.euler.euler2mat(ai, aj, ak, axes='sxyz'),
        Z=np.ones(3)
    )
    obj = dict(
        label=mesh_name,
        urdf_path=urdf_path,
        scale=cfg.scale,
        TWO=TWO, # object pose in world coordinate
    )
    return obj

def main(cfg):
    cam = set_cam_info(cfg.CAM_INFO)
    obj = set_mesh_info(cfg.MESH_INFO)
    # rendering
    renderer = BulletSceneRenderer(background_color=cfg.RENDERER_INFO.background_color, 
                                    gpu_renderer=cfg.RENDERER_INFO.use_gpu, 
                                    gui=cfg.RENDERER_INFO.gui)
    cam_obs = renderer.render_scene([obj], [cam], render_depth=cfg.RENDERER_INFO.depth)

    rgb = cam_obs[0]['rgb']
    depth = cam_obs[0]['depth']
    mask = cam_obs[0]['mask']
    K = cam_obs[0]['K']

    ## saving result ###
    import cv2
    import shutil
    from pathlib import Path
    output_dir = Path(cfg.OUTPUT_DIR)
    if output_dir.is_dir():
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
    else:
        os.makedirs(output_dir)

    cv2.imwrite(os.path.join(cfg.OUTPUT_DIR,'rgb.png'), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite(os.path.join(cfg.OUTPUT_DIR,'mask.png'), mask)
    if cfg.RENDERER_INFO.depth:
        cv2.imwrite(os.path.join(cfg.OUTPUT_DIR,'depth.png'), depth)

    # depth_o3d = o3d.geometry.Image(depth)
    # pointcloud = o3d.geometry.PointCloud.create_from_depth_image(depth_o3d,
    #         o3d.camera.PinholeCameraIntrinsic(resolution[0], resolution[1], fx, fy, cx, cy)
    #         )
    # o3d.io.write_point_cloud('./images/pcd.ply', pointcloud)
    # o3d.visualization.draw_geometries([pointcloud])

    # # debug show
    # plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.imshow(rgb)
    # plt.subplot(1, 2, 2)
    # plt.imshow(mask)
    # plt.show()

if __name__ == '__main__':
    args = get_parser()
    cfg = Config.fromfile(args.config)
    cfg.RENDERER_INFO['use_gpu'] = args.use_gpu

    if args.use_gpu:
        os.environ['CUDA_VISIBLE_DEVICES']='0'

    main(cfg)