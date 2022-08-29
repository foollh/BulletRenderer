import numpy as np
import transforms3d
import open3d as o3d
from rendering.bullet_scene_renderer import BulletSceneRenderer
from matplotlib import pyplot as plt

TCO = transforms3d.affines.compose(
    T=[0, 0, 0.25],
    R=transforms3d.euler.euler2mat(0, np.pi/2, 0, axes='sxyz'),
    Z=np.ones(3)
)

fx, fy = 300, 300
cx, cy = 320, 240
K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])

cam = dict(
    resolution=(640, 480),
    K=K,
    TWC=np.eye(4)
)

obj_mesh = o3d.io.read_triangle_mesh('/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/obj_000007.ply')
obj = dict(
    label='obj_000007',
    mesh=obj_mesh,
    # urdf_path='/home/lihua/Desktop/Repositories/Github_Copy/PoseEstimation/RobotPoseEstimation/robopose/local_data/urdfs/lm/obj_000007/obj_000007.urdf',
    # urdf_path='/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/OBJ/obj_000007.urdf',
    scale=0.001,
    TWO=TCO,
)

# rendering
renderer = BulletSceneRenderer(background_color=(0, 0, 0), gpu_renderer=True, gui=True)
cam_obs = renderer.render_scene([obj], [cam], render_depth=True)

rgb = cam_obs[0]['rgb']
depth = cam_obs[0]['depth']
mask = cam_obs[0]['mask']
K = cam_obs[0]['K']

# debug show
plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(rgb)

plt.subplot(1, 2, 2)
plt.imshow(mask)

plt.show()