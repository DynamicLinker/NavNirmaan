import bpy
import sys

def main():
    bpy.ops.wm.open_mainfile(filepath="interactive.blend")
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            print(f"Object: {obj.name}")
            if obj.data.materials:
                mat = obj.data.materials[0]
                if mat.use_nodes and 'Principled BSDF' in mat.node_tree.nodes:
                    c = mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value
                    print(f"  Color: {c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f}")
            wm = obj.matrix_world
            verts = [wm @ v.co for v in obj.data.vertices]
            if verts:
                xs = [v.x for v in verts]
                ys = [v.y for v in verts]
                zs = [v.z for v in verts]
                dx = max(xs) - min(xs)
                dy = max(ys) - min(ys)
                dz = max(zs) - min(zs)
                z0 = min(zs)
                print(f"  Bounds: dx={dx:.2f}, dy={dy:.2f}, dz={dz:.2f}, z0={z0:.2f}")

if __name__ == "__main__":
    main()
