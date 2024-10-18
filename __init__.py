bl_info = {
    "name": "Vertex Color Map",
    "author": "maxxniono",
    "version": (0, 0, 1),
    "blender": (4, 2, 0),
    "location": "Edit | MVC",
    "description": "Tools for manipulating vertex color data.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/maxxnino/VertexColorMap/issues",
    "category": "Mesh",
}

import bpy

class MESH_OT_set_vertex_color(bpy.types.Operator):
    """Set vertex color of selected vertices"""
    bl_idname = "mesh.max_vertex_color"  # Operator name for the context menu
    bl_label = "Set Vertex Color"  # Operator label
    bl_options = {'REGISTER', 'UNDO'}  # Allows for undo functionality

    # Define properties to accept user input
    index: bpy.props.IntProperty(
        name="Channel Index",
        description="Color Channel",
        default=1
    )
    
    def execute(self, context):
        # Make sure you're in 'EDIT' mode
        # channel_index = self.args 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the active object
        obj = context.active_object

        # Ensure the object is a mesh
        if obj and obj.type == 'MESH':
            # Get the mesh data
            mesh = obj.data

            # Check if the mesh has vertex color layers
            # color_attribute = mesh.color_attributes.get("Color")
            if not mesh.vertex_colors:
                print("No vertex color layers found, adding a new one.")
                color_attr = mesh.color_attributes.new("Color", 'BYTE_COLOR', 'CORNER')
                for poly in obj.data.polygons:
                    for loop_index in poly.loop_indices:  # Access the loop indices of the polygon
                        color_attr.data[loop_index].color = (0, 0, 0, 255)

            # Get the active vertex color layer
            vertex_colors = mesh.vertex_colors.active.data
            # Get the vertex selection data (based on the vertex indices)
            selected_verts = [v for v in mesh.vertices if v.select]

            # Check if there are selected vertices
            if selected_verts:
                # Loop through the loops (polygons) and modify only selected vertices
                for loop_index, loop in enumerate(mesh.loops):
                    vertex_index = loop.vertex_index

                    # If the vertex is selected, modify its color
                    if mesh.vertices[vertex_index].select:
                        color = vertex_colors[loop_index].color
                        
                        # Modify the red channel (0: red, 1: green, 2: blue, 3: alpha)
                        color[self.index] = context.scene.my_addon_value  # Example: set the red channel to 0.5
                        
                        # Optionally modify other channels
                        # color[1] = 0.0  # Green channel
                        # color[2] = 1.0  # Blue channel
            else:
                print("No vertices are selected.")

            # Update the mesh after modifying vertex colors
            mesh.update()
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


# Define the custom panel class
class VIEW3D_PT_my_edit_mode_panel(bpy.types.Panel):
    bl_label = "Vertex Color Panel"
    bl_idname = "Maxx_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VCM'
    
    # Panel only appears when in Edit Mode
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "my_addon_value")
        row = layout.row()

        # Example of adding a button to the panel
        col = row.column(align=False)
        ao_op = col.operator("mesh.max_vertex_color", text="AO")
        ao_op.index = 0
        # ao_op.value = self.value

        col = row.row(align=False)
        edge_op = col.operator("mesh.max_vertex_color", text="Edge")
        edge_op.index = 1
        # edge_op.value = self.value

        row = layout.row()

        col = row.row(align=False)
        metallic_op = col.operator("mesh.max_vertex_color", text="Matallic")
        metallic_op.index = 2
        # metallic_op.value = self.value

        col = row.row(align=False)
        rough_op = col.operator("mesh.max_vertex_color", text="Roughness")
        rough_op.index = 3
        # rough_op.value = self.value

# Registering the custom panel
def register():
    bpy.types.Scene.my_addon_value = bpy.props.FloatProperty(
        name="Value",
        description="color value",
        default=0.5,
        min=0.0,
        max=1.0
    )

    bpy.utils.register_class(MESH_OT_set_vertex_color)
    bpy.utils.register_class(VIEW3D_PT_my_edit_mode_panel)

# Unregistering the custom panel
def unregister():
    del bpy.types.Scene.my_addon_value
    bpy.utils.unregister_class(MESH_OT_set_vertex_color)
    bpy.utils.unregister_class(VIEW3D_PT_my_edit_mode_panel)

if __name__ == "__main__":
    register()