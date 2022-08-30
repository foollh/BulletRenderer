import numpy as np
import transforms3d
import open3d as o3d
from rendering.bullet_scene_renderer import BulletSceneRenderer
from matplotlib import pyplot as plt

# camera intrinsic param set
fx, fy = 300, 300
cx, cy = 320, 240
K = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
])
# camera information set
resolution = (640, 480)
cam = dict(
    resolution=resolution,
    K=K,
    TWC=np.eye(4)  # camera pose in world coordinate
)

# object information set
obj_mesh = o3d.io.read_triangle_mesh('/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/obj_000009.ply')
TCO = transforms3d.affines.compose(
    T=[0, 0, 0.25],
    R=transforms3d.euler.euler2mat(np.pi/2, 0, 0, axes='sxyz'),
    Z=np.ones(3)
)
obj = dict(
    label='obj_000007',
    mesh=obj_mesh,  # object mesh(o3d.geometry.TriangelMesh)
    scale=0.001,
    TWO=TCO, # object pose in world coordinate
)

# rendering
renderer = BulletSceneRenderer(background_color=(0, 0, 0), gpu_renderer=True, gui=True)
cam_obs = renderer.render_scene([obj], [cam], render_depth=True)

rgb = cam_obs[0]['rgb']
depth = cam_obs[0]['depth']
mask = cam_obs[0]['mask']
K = cam_obs[0]['K']

### saving result ###
# import cv2
# cv2.imwrite('./images/rgb.png', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
# cv2.imwrite('./images/mask.png', mask)
# cv2.imwrite('./images/depth.png', depth)
# depth_o3d = o3d.geometry.Image(depth)
# pointcloud = o3d.geometry.PointCloud.create_from_depth_image(
#         depth_o3d,
#         o3d.camera.PinholeCameraIntrinsic(
#             resolution[0], resolution[1], 
#             fx, fy,
#             cx, cy
#             )
#         )
# o3d.io.write_point_cloud('./images/pcd.ply', pointcloud)
# o3d.visualization.draw_geometries([pointcloud])

# debug show
plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(rgb)

plt.subplot(1, 2, 2)
plt.imshow(mask)

plt.show()