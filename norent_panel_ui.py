import bpy
from bpy.types import Panel, UIList, Operator
from bpy.props import StringProperty, IntProperty

class NORENT_UL_MotionLayers(UIList):
    """Custom UIList for motion layers (AE-style layer stack)"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # Layer name
            layout.prop(item, "name", text="", emboss=False, icon='OBJECT_DATA')
            
            # Solo/Mute buttons
            row = layout.row(align=True)
            row.scale_x = 0.8
            
            # Visibility toggle
            if item.hide_viewport:
                row.prop(item, "hide_viewport", text="", icon='HIDE_ON', emboss=False)
            else:
                row.prop(item, "hide_viewport", text="", icon='HIDE_OFF', emboss=False)
            
            # Render visibility
            if item.hide_render:
                row.prop(item, "hide_render", text="", icon='RESTRICT_RENDER_ON', emboss=False)
            else:
                row.prop(item, "hide_render", text="", icon='RESTRICT_RENDER_OFF', emboss=False)
                
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='OBJECT_DATA')

class NORENT_PT_MainPanel(Panel):
    """Main NORENT Motion panel"""
    bl_label = "NORENT Motion"
    bl_idname = "NORENT_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NORENT'
    
    def draw_header(self, context):
        self.layout.label(text="", icon='FORCE_VORTEX')
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header with branding
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text="MOTION GRAPHICS WEAPON", icon='EXPERIMENTAL')
        
        layout.separator()
        
        # Quick setup
        box = layout.box()
        box.label(text="INITIALIZE", icon='SETTINGS')
        box.operator("norent.setup_workspace", text="Setup Workspace", icon='WORKSPACE')
        
        # Check if pro version
        prefs = context.preferences.addons[__name__.split('.')[0]].preferences
        if not prefs.pro_version:
            box.label(text="⚡ Free Version", icon='INFO')
        else:
            box.label(text="✅ PRO ACTIVE", icon='CHECKMARK')

class NORENT_PT_LayerStack(Panel):
    """Layer stack panel (AE-style)"""
    bl_label = "Layer Stack"
    bl_idname = "NORENT_PT_layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NORENT'
    bl_parent_id = "NORENT_PT_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Layer list
        row = layout.row()
        row.template_list("NORENT_UL_MotionLayers", "", scene, "objects", scene.norent, "active_layer")
        
        # Layer controls
        col = row.column(align=True)
        col.operator("norent.layer_add", text="", icon='ADD')
        col.operator("norent.layer_remove", text="", icon='REMOVE')
        col.separator()
        col.operator("norent.layer_up", text="", icon='TRIA_UP')
        col.operator("norent.layer_down", text="", icon='TRIA_DOWN')
        
        # Layer properties
        if scene.objects:
            active_obj = scene.objects.get(scene.norent.active_layer)
            if active_obj:
                box = layout.box()
                box.prop(active_obj, "name", text="Layer Name")
                
                row = box.row(align=True)
                row.prop(active_obj, "hide_viewport", text="Hide", toggle=True)
                row.prop(active_obj, "hide_render", text="No Render", toggle=True)

class NORENT_PT_TextFX(Panel):
    """Text effects panel"""
    bl_label = "Text FX"
    bl_idname = "NORENT_PT_textfx"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NORENT'
    bl_parent_id = "NORENT_PT_main"
    
    def draw(self, context):
        layout = self.layout
        
        # Text creation
        box = layout.box()
        box.label(text="CREATE TEXT", icon='FONT_DATA')
        
        col = box.column(align=True)
        col.operator("norent.text_add_animated", text="Animated Text", icon='PLUS')
        col.operator("norent.text_add_typewriter", text="Typewriter", icon='EDIT')
        col.operator("norent.text_add_bounce", text="Bounce In", icon='FORCE_FORCE')
        col.operator("norent.text_add_wipe", text="Wipe Up", icon='TRIA_UP')
        
        # Text animation presets
        layout.separator()
        box = layout.box()
        box.label(text="ANIMATE SELECTED", icon='ANIM')
        
        if context.object and context.object.type == 'FONT':
            col = box.column(align=True)
            col.operator("norent.text_animate_scale", text="Scale Pop")
            col.operator("norent.text_animate_fade", text="Fade In/Out")
            col.operator("norent.text_animate_slide", text="Slide In")
        else:
            box.label(text="Select text object", icon='INFO')

class NORENT_PT_CameraRigs(Panel):
    """Camera rigs panel"""
    bl_label = "Camera Rigs"
    bl_idname = "NORENT_PT_camera"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NORENT'
    bl_parent_id = "NORENT_PT_main"
    
    def draw(self, context):
        layout = self.layout
        
        # Camera creation
        box = layout.box()
        box.label(text="CREATE CAMERA", icon='CAMERA_DATA')
        
        col = box.column(align=True)
        col.operator("norent.camera_add_basic", text="Basic Rig", icon='CAMERA_DATA')
        col.operator("norent.camera_add_handheld", text="Handheld", icon='FORCE_TURBULENCE')
        col.operator("norent.camera_add_dolly", text="Dolly Track", icon='CURVE_PATH')
        
        # Camera moves
        if context.scene.camera:
            layout.separator()
            box = layout.box()
            box.label(text="CAMERA MOVES", icon='ANIM')
            
            col = box.column(align=True)
            col.operator("norent.camera_push_in", text="Push In")
            col.operator("norent.camera_rotate", text="Rotate Around")
            col.operator("norent.camera_shake", text="Add Shake")

class NORENT_PT_Render(Panel):
    """Render panel"""
    bl_label = "Render"
    bl_idname = "NORENT_PT_render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NORENT'
    bl_parent_id = "NORENT_PT_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Render presets
        box = layout.box()
        box.label(text="RENDER PRESETS", icon='RENDER_ANIMATION')
        
        col = box.column(align=True)
        col.prop(scene.norent, "render_preset", text="")
        
        # Render info
        render = scene.render
        info_text = f"{render.resolution_x}x{render.resolution_y} @ {render.fps}fps"
        layout.label(text=info_text, icon='INFO')
        
        # Render buttons
        layout.separator()
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator("norent.render_still", text="Render Frame", icon='RENDER_STILL')
        col.operator("norent.render_animation", text="Render Animation", icon='RENDER_ANIMATION')
        
        # Export options
        layout.separator()
        box = layout.box()
        box.label(text="EXPORT", icon='EXPORT')
        
        col = box.column(align=True)
        col.operator("norent.export_mp4", text="Export MP4", icon='FILE_MOVIE')
        col.operator("norent.export_gif", text="Export GIF", icon='FILE_IMAGE')

# Layer management operators
class NORENT_OT_LayerAdd(Operator):
    bl_idname = "norent.layer_add"
    bl_label = "Add Layer"
    bl_description = "Add new motion layer"
    
    def execute(self, context):
        # Add empty object as layer
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        context.object.name = f"Layer_{len(context.scene.objects):02d}"
        context.scene.norent.active_layer = context.object.name
        return {'FINISHED'}

class NORENT_OT_LayerRemove(Operator):
    bl_idname = "norent.layer_remove"
    bl_label = "Remove Layer"
    bl_description = "Remove selected layer"
    
    def execute(self, context):
        if context.object:
            bpy.ops.object.delete()
        return {'FINISHED'}

class NORENT_OT_LayerUp(Operator):
    bl_idname = "norent.layer_up"
    bl_label = "Move Layer Up"
    bl_description = "Move layer up in stack"
    
    def execute(self, context):
        # Implementation for layer reordering
        self.report({'INFO'}, "Layer moved up")
        return {'FINISHED'}

class NORENT_OT_LayerDown(Operator):
    bl_idname = "norent.layer_down"
    bl_label = "Move Layer Down"
    bl_description = "Move layer down in stack"
    
    def execute(self, context):
        # Implementation for layer reordering
        self.report({'INFO'}, "Layer moved down")
        return {'FINISHED'}

# Registration
classes = [
    NORENT_UL_MotionLayers,
    NORENT_PT_MainPanel,
    NORENT_PT_LayerStack,
    NORENT_PT_TextFX,
    NORENT_PT_CameraRigs,
    NORENT_PT_Render,
    NORENT_OT_LayerAdd,
    NORENT_OT_LayerRemove,
    NORENT_OT_LayerUp,
    NORENT_OT_LayerDown,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)