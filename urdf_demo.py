import numpy as np
import open3d as o3d
from libmesh import ply_to_obj, obj_to_urdf


ply_path = '/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/obj_000007.ply'
obj_path = '/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/OBJ/obj_000007.obj'
urdf_path = '/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/OBJ/obj_000007.urdf'

# ply_to_obj(ply_path=ply_path, obj_path=obj_path)

mesh = o3d.io.read_triangle_mesh(ply_path)
o3d.io.write_triangle_mesh(obj_path, mesh)

obj_to_urdf(obj_path=obj_path, urdf_path=urdf_path)
