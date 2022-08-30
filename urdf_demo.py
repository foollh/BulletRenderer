from libmesh import ply_to_obj, obj_to_urdf

ply_path = '/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/obj_000009.ply'
obj_path = '/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/OBJ/obj_000009.obj'
urdf_path = '/home/lihua/Desktop/Datasets/LINEMOD/lm_models/models/OBJ/obj_000009.urdf'

# meshlabserver -i obj_000009.ply -o obj_000009.obj -m wt -s texture_generate.mlx

ply_to_obj(ply_path=ply_path, obj_path=obj_path)

obj_to_urdf(obj_path=obj_path, urdf_path=urdf_path)
