from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom
import trimesh
# from urdfpytorch.utils import unparse_origin, parse_origin
from .meshlab_converter import ply_to_obj


def resolve_package_path(urdf_path, mesh_path):
    urdf_path = Path(urdf_path)
    search_dir = urdf_path.parent
    relative_path = Path(str(mesh_path).replace('package://', ''))
    while True:
        absolute_path = (search_dir / relative_path)
        if absolute_path.exists():
            return absolute_path
        search_dir = search_dir.parent


def extract_mesh_visuals(mesh):
    visuals = []
    graph = mesh.graph
    geometries = mesh.geometry
    for node_id, node_infos in graph.to_flattened().items():
        geometry = node_infos.get('geometry')
        if geometry is not None:
            visuals.append((geometries[geometry], node_infos['transform']))
    return visuals


def obj_to_urdf(obj_path, urdf_path):
    obj_path = Path(obj_path)
    urdf_path = Path(urdf_path)
    assert urdf_path.parent == obj_path.parent

    geometry = ET.Element('geometry')
    mesh = ET.SubElement(geometry, 'mesh')
    mesh.set('filename', obj_path.name)
    mesh.set('scale', '1.0 1.0 1.0')

    material = ET.Element('material')
    material.set('name', 'mat_part0')
    color = ET.SubElement(material, 'color')
    color.set('rgba', '1.0 1.0 1.0 1.0')

    inertial = ET.Element('inertial')
    origin = ET.SubElement(inertial, 'origin')
    origin.set('rpy', '0 0 0')
    origin.set('xyz', '0.0 0.0 0.0')

    mass = ET.SubElement(inertial, 'mass')
    mass.set('value', '0.1')

    inertia = ET.SubElement(inertial, 'inertia')
    inertia.set('ixx', '1')
    inertia.set('ixy', '0')
    inertia.set('ixz', '0')
    inertia.set('iyy', '1')
    inertia.set('iyz', '0')
    inertia.set('izz', '1')

    robot = ET.Element('robot')
    robot.set('name', obj_path.with_suffix('').name)

    link = ET.SubElement(robot, 'link')
    link.set('name', 'base_link')

    visual = ET.SubElement(link, 'visual')
    visual.append(geometry)
    visual.append(material)

    collision = ET.SubElement(link, 'collision')
    collision.append(geometry)

    link.append(inertial)

    xmlstr = minidom.parseString(ET.tostring(robot)).toprettyxml(indent="   ")
    Path(urdf_path).write_text(xmlstr)  # Write xml file
    return


