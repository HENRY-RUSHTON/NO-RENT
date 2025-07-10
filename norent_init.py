bl_info = {
    "name": "NORENT Motion",
    "author": "NORENT Labs",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > NORENT",
    "description": "Cultural weapon disguised as motion graphics tools",
    "category": "Animation",
    "doc_url": "https://norent.tools/motion",
    "tracker_url": "https://github.com/norent/motion/issues"
}

import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import BoolProperty, StringProperty, EnumProperty

# Import our modules
from . import panel_ui
from . import text_fx
from . import camera_rigs
from . import easing
from . import utils

# Add-on preferences
class NorentPreferences(AddonPreferences):
    bl_idname = __name__
    
    pro_version: BoolProperty(
        name="Pro Version Unlocked",
        description="Enable advanced features",
        default=False
    )
    
    license_key: StringProperty(
        name="License Key",
        description="Enter your NORENT Motion Pro license key",
        default=""
    )
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="NORENT Motion Configuration", icon='SETTINGS')
        
        if self.pro_version:
            layout.label(text="✅ PRO VERSION ACTIVE", icon='CHECKMARK')
        else:
            layout.label(text="⚡ Free Version - Upgrade for advanced features")
            
        layout.prop(self, "license_key")
        layout.operator("norent.validate_license", text="Validate License")

# Scene properties
class NorentSceneProperties(PropertyGroup):
    active_layer: StringProperty(
        name="Active Layer",
        description="Currently selected motion layer",
        default=""
    )
    
    render_preset: EnumProperty(
        name="Render Preset",
        description="Quick render configurations",
        items=[
            ('REEL', "Instagram Reel", "1080x1920 vertical"),
            ('SQUARE', "Square Post", "1080x1080 square"),
            ('STORY', "Story/TikTok", "1080x1920 vertical"),
            ('LANDSCAPE', "Landscape", "1920x1080 horizontal"),
            ('CUSTOM', "Custom", "Use current render settings")
        ],
        default='REEL'
    )

# License validation operator
class NORENT_OT_ValidateLicense(bpy.types.Operator):
    bl_idname = "norent.validate_license"
    bl_label = "Validate License"
    bl_description = "Validate your NORENT Motion Pro license"
    
    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        
        # Mock license validation - replace with actual API call
        if prefs.license_key.startswith("NORENT_PRO_"):
            prefs.pro_version = True
            self.report({'INFO'}, "License validated - Pro features unlocked!")
        else:
            prefs.pro_version = False
            self.report({'WARNING'}, "Invalid license key")
            
        return {'FINISHED'}

# Auto-setup workspace
class NORENT_OT_SetupWorkspace(bpy.types.Operator):
    bl_idname = "norent.setup_workspace"
    bl_label = "Setup NORENT Workspace"
    bl_description = "Configure Blender workspace for motion graphics"
    
    def execute(self, context):
        # Create custom workspace if it doesn't exist
        workspace_name = "NORENT Motion"
        
        if workspace_name not in bpy.data.workspaces:
            # Duplicate Animation workspace as base
            bpy.ops.workspace.duplicate({'workspace': bpy.data.workspaces['Animation']})
            bpy.context.workspace.name = workspace_name
            
            # Configure timeline to show more frames
            for screen in bpy.context.workspace.screens:
                for area in screen.areas:
                    if area.type == 'TIMELINE':
                        area.spaces[0].show_seconds = False
                        area.spaces[0].show_frame_indicator = True
                    elif area.type == 'VIEW_3D':
                        # Set viewport shading to material preview
                        area.spaces[0].shading.type = 'MATERIAL'
                        
        # Switch to our workspace
        bpy.context.window.workspace = bpy.data.workspaces[workspace_name]
        
        # Set render settings for motion graphics
        scene = context.scene
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1920
        scene.render.fps = 30
        scene.frame_end = 300  # 10 seconds at 30fps
        
        # Set up timeline
        scene.frame_start = 1
        scene.frame_current = 1
        
        self.report({'INFO'}, f"NORENT Motion workspace configured")
        return {'FINISHED'}

# Registration
classes = [
    NorentPreferences,
    NorentSceneProperties,
    NORENT_OT_ValidateLicense,
    NORENT_OT_SetupWorkspace,
]

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register modules
    panel_ui.register()
    text_fx.register()
    camera_rigs.register()
    easing.register()
    utils.register()
    
    # Add scene properties
    bpy.types.Scene.norent = bpy.props.PointerProperty(type=NorentSceneProperties)
    
    # Auto-setup workspace on install
    bpy.app.timers.register(lambda: bpy.ops.norent.setup_workspace(), first_interval=1.0)

def unregister():
    # Unregister modules
    utils.unregister()
    easing.unregister()
    camera_rigs.unregister()
    text_fx.unregister()
    panel_ui.unregister()
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove scene properties
    del bpy.types.Scene.norent

if __name__ == "__main__":
    register()