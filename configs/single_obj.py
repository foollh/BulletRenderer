OUTPUT_DIR = "./cache/"
# camera information
CAM_INFO = dict(
    resolution=(640, 480),
    fx_fy=(300, 300),
    cx_cy=(320, 240),
    angle=[0, 0, 0],  # camera rotation in world coordinate (degrees sxyz)
    trans=[0, 0, 0],  # camera translation in world coordinate
)

# mesh information
MESH_INFO = dict(
    # urdf_path='/cluster/ws_download/liu.lihua/MegaPose-GSO/Google_Scanned_Objects/11pro_SL_TRX_FG/meshes/model.urdf'
    mesh_path='/cluster/ws_download/liu.lihua/MegaPose-GSO/Google_Scanned_Objects/11pro_SL_TRX_FG/meshes/model.obj',
    scale=1,
    angle=[0, 90, 0],  # mesh rotation in world coordinate (degrees sxyz)
    trans=[0, 0, 0.25],  # mesh translation in world coordinate
)

# renderer information
RENDERER_INFO = dict(
    gui=False,
    depth=False,
    background_color=(0, 0, 0),
)