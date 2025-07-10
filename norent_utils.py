import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty, BoolProperty
from mathutils import Vector

class NORENT_OT_RenderStill(Operator):
    """Render current frame with preset settings"""
    bl_idname = "norent.render_still"
    bl_label = "Render Still"
    bl_description = "Render current frame with NORENT settings"
    
    def execute(self, context):
        # Apply render preset
        self.apply_render_preset(context)
        
        # Render
        bpy.ops.render.render(use_viewport=True)
        
        self.report({'INFO'}, "Still frame rendered")
        return {'FINISHED'}
    
    def apply_render_preset(self, context):
        """Apply render settings based on preset"""
        scene = context.scene
        render = scene.render
        preset = scene.norent.render_preset
        
        if preset == 'REEL':
            render.resolution_x = 1080
            render.resolution_y = 1920
            render.fps = 30
        elif preset == 'SQUARE':
            render.resolution_x = 1080
            render.resolution_y = 1080
            render.fps = 30
        elif preset == 'STORY':
            render.resolution_x = 1080
            render.resolution_y = 1920
            render.fps = 30
        elif preset == 'LANDSCAPE':
            render.resolution_x = 1920
            render.resolution_y = 1080
            render.fps = 30
        
        # Set output format
        render.image_settings.file_format = 'PNG'
        render.image_settings.color_mode = 'RGBA'

class NORENT_OT_RenderAnimation(Operator):
    """Render animation with preset settings"""
    bl_idname = "norent.render_animation"
    bl_label = "Render Animation"
    bl_description = "Render full animation with NORENT settings"
    
    def execute(self, context):
        # Apply render preset
        self.apply_render_preset(context)
        
        # Set output path
        self.set_output_path(context)
        
        # Render animation
        bpy.ops.render.render(animation=True)
        
        self.report({'INFO'}, "Animation render started")
        return {'FINISHED'}
    
    def apply_render_preset(self, context):
        """Apply render settings based on preset"""
        scene = context.scene
        render = scene.render
        preset = scene.norent.render_preset
        
        if preset == 'REEL':
            render.resolution_x = 1080
            render.resolution_y = 1920
            render.fps = 30
        elif preset == 'SQUARE':
            render.resolution_x = 1080
            render.resolution_y = 1080
            render.fps = 30
        elif preset == 'STORY':
            render.resolution_x = 1080
            render.resolution_y = 1920
            render.fps = 30
        elif preset == 'LANDSCAPE':
            render.resolution_x = 1920
            render.resolution_y = 1080
            render.fps = 30
        
        # Set output format for animation
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'MPEG4'
        render.ffmpeg.codec = 'H264'
        render.ffmpeg.constant_rate_factor = 'HIGH'
    
    def set_output_path(self, context):
        """Set appropriate output path"""
        scene = context.scene
        preset = scene.norent.render_preset
        
        # Create NORENT output directory
        output_dir = os.path.join(bpy.path.abspath("//"), "NORENT_Renders")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set filename based on preset
        filename = f"NORENT_{preset}_{scene.name}"
        scene.render.filepath = os.path.join(output_dir, filename)

class NORENT_OT_ExportMP4(Operator):
    """Export animation as MP4"""
    bl_idname = "norent.export_mp4"
    bl_label = "Export MP4"
    bl_description = "Export animation as MP4 file"
    
    def execute(self, context):
        scene = context.scene
        render = scene.render
        
        # Store original settings
        original_format = render.image_settings.file_format
        original_ffmpeg_format = render.ffmpeg.format
        original_codec = render.ffmpeg.codec
        
        # Set MP4 settings
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'MPEG4'
        render.ffmpeg.codec = 'H264'
        render.ffmpeg.constant_rate_factor = 'HIGH'
        
        # Set output path
        preset = scene.norent.render_preset
        output_dir = os.path.join(bpy.path.abspath("//"), "NORENT_Exports")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = f"NORENT_{preset}_{scene.name}.mp4"
        render.filepath = os.path.join(output_dir, filename)
        
        # Render
        bpy.ops.render.render(animation=True)
        
        # Restore original settings
        render.image_settings.file_format = original_format
        render.ffmpeg.format = original_ffmpeg_format
        render.ffmpeg.codec = original_codec
        
        self.report({'INFO'}, f"MP4 exported to {filename}")
        return {'FINISHED'}

class NORENT_OT_ExportGIF(Operator):
    """Export animation as GIF"""
    bl_idname = "norent.export_gif"
    bl_label = "Export GIF"
    bl_description = "Export animation as GIF file"
    
    quality: EnumProperty(
        name="Quality",
        description="GIF quality preset",
        items=[
            ('HIGH', "High", "Best quality, larger file"),
            ('MEDIUM', "Medium", "Balanced quality and size"),
            ('LOW', "Low", "Smaller file, lower quality")
        ],
        default='MEDIUM'
    )
    
    def execute(self, context):
        scene = context.scene
        render = scene.render
        
        # Store original settings
        original_format = render.image_settings.file_format
        original_res_x = render.resolution_x
        original_res_y = render.resolution_y
        
        # Set GIF-appropriate settings
        if self.quality == 'HIGH':
            scale = 1.0
        elif self.quality == 'MEDIUM':
            scale = 0.75
        else:  # LOW
            scale = 0.5
        
        render.resolution_x = int(original_res_x * scale)
        render.resolution_y = int(original_res_y * scale)
        render.image_settings.file_format = 'PNG'
        
        # Set output path for frames
        output_dir = os.path.join(bpy.path.abspath("//"), "NORENT_GIF_Frames")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        render.filepath = os.path.join(output_dir, "frame_")
        
        # Render frames
        bpy.ops.render.render(animation=True)
        
        # Note: Actual GIF creation would require external tool like ffmpeg
        # This is a placeholder for the frame export process
        
        # Restore original settings
        render.image_settings.file_format = original_format
        render.resolution_x = original_res_x
        render.resolution_y = original_res_y
        
        self.report({'INFO'}, f"GIF frames exported ({self.quality} quality)")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_LoadTemplate(Operator):
    """Load animation template"""
    bl_idname = "norent.load_template"
    bl_label = "Load Template"
    bl_description = "Load pre-made animation template"
    
    template_name: EnumProperty(
        name="Template",
        description="Choose template to load",
        items=[
            ('LOWER_THIRD', "Lower Third", "Lower third text overlay"),
            ('LYRIC_VIDEO', "Lyric Video", "Lyric video template"),
            ('INTRO_SPLASH', "Intro Splash", "Brand intro template"),
            ('TRANSITION', "Transition", "Scene transition pack"),
            ('LOGO_REVEAL', "Logo Reveal", "Logo animation template")
        ],
        default='LOWER_THIRD'
    )
    
    replace_scene: BoolProperty(
        name="Replace Current Scene",
        description="Replace current scene or append to it",
        default=False
    )
    
    def execute(self, context):
        # Get addon directory
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        templates_dir = os.path.join(addon_dir, "templates")
        
        # Template file mapping
        template_files = {
            'LOWER_THIRD': "lower_third.blend",
            'LYRIC_VIDEO': "lyric_video.blend",
            'INTRO_SPLASH': "intro_splash.blend",
            'TRANSITION': "transition_pack.blend",
            'LOGO_REVEAL': "logo_reveal.blend"
        }
        
        template_file = template_files.get(self.template_name)
        if not template_file:
            self.report({'ERROR'}, "Template not found")
            return {'CANCELLED'}
        
        template_path = os.path.join(templates_dir, template_file)
        
        if not os.path.exists(template_path):
            self.report({'ERROR'}, f"Template file not found: {template_file}")
            return {'CANCELLED'}
        
        if self.replace_scene:
            # Clear current scene
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
        
        # Append template objects
        with bpy.data.libraries.load(template_path) as (data_from, data_to):
            data_to.objects = data_from.objects
            data_to.materials = data_from.materials
            data_to.node_groups = data_from.node_groups
        
        # Link objects to scene
        for obj in data_to.objects:
            if obj:
                context.collection.objects.link(obj)
        
        self.report({'INFO'}, f"Template '{self.template_name}' loaded")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_SaveTemplate(Operator):
    """Save current scene as template"""
    bl_idname = "norent.save_template"
    bl_label = "Save Template"
    bl_description = "Save current scene as reusable template"
    
    template_name: StringProperty(
        name="Template Name",
        description="Name for the template",
        default="My_Template"
    )
    
    def execute(self, context):
        # Get addon directory
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        templates_dir = os.path.join(addon_dir, "templates")
        
        # Create templates directory if it doesn't exist
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        # Clean template name
        clean_name = "".join(c for c in self.template_name if c.isalnum() or c in "._-")
        template_file = f"{clean_name}.blend"
        template_path = os.path.join(templates_dir, template_file)
        
        # Save current file as template
        bpy.ops.wm.save_as_mainfile(filepath=template_path, copy=True)
        
        self.report({'INFO'}, f"Template saved as '{template_file}'")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_OptimizeScene(Operator):
    """Optimize scene for motion graphics"""
    bl_idname = "norent.optimize_scene"
    bl_label = "Optimize Scene"
    bl_description = "Optimize scene settings for motion graphics workflow"
    
    def execute(self, context):
        scene = context.scene
        
        # Set optimal timeline settings
        scene.frame_start = 1
        if scene.frame_end < 300:
            scene.frame_end = 300  # 10 seconds at 30fps
        
        # Optimize render settings
        render = scene.render
        render.use_motion_blur = False  # Disable for faster preview
        render.use_freestyle = False    # Disable unless needed
        
        # Set viewport settings for performance
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces[0]
                space.shading.type = 'MATERIAL'
                space.overlay.show_wireframes = False
                space.overlay.show_floor = False
                space.overlay.show_axis_x = False
                space.overlay.show_axis_y = False
        
        # Enable auto-keyframe
        scene.tool_settings.use_keyframe_insert_auto = True
        
        # Set better keyframe defaults
        scene.tool_settings.keyframe_type = 'KEYFRAME'
        
        self.report({'INFO'}, "Scene optimized for motion graphics")
        return {'FINISHED'}

class NORENT_OT_QuickPreview(Operator):
    """Quick viewport render preview"""
    bl_idname = "norent.quick_preview"
    bl_label = "Quick Preview"
    bl_description = "Generate quick preview of current animation"
    
    frame_step: EnumProperty(
        name="Frame Step",
        description="Skip frames for faster preview",
        items=[
            ('1', "Every Frame", "Render every frame"),
            ('2', "Every 2nd Frame", "Skip every other frame"),
            ('3', "Every 3rd Frame", "Skip 2 frames"),
            ('5', "Every 5th Frame", "Skip 4 frames")
        ],
        default='2'
    )
    
    def execute(self, context):
        scene = context.scene
        
        # Store original settings
        original_step = scene.frame_step
        original_format = scene.render.image_settings.file_format
        original_res_x = scene.render.resolution_x
        original_res_y = scene.render.resolution_y
        
        # Set preview settings
        scene.frame_step = int(self.frame_step)
        scene.render.resolution_x = int(original_res_x * 0.5)  # Half resolution for speed
        scene.render.resolution_y = int(original_res_y * 0.5)
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        
        # Set output path
        output_dir = os.path.join(bpy.path.abspath("//"), "NORENT_Previews")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = f"NORENT_Preview_{scene.name}"
        scene.render.filepath = os.path.join(output_dir, filename)
        
        # Render preview
        bpy.ops.render.render(animation=True)
        
        # Restore original settings
        scene.frame_step = original_step
        scene.render.resolution_x = original_res_x
        scene.render.resolution_y = original_res_y
        scene.render.image_settings.file_format = original_format
        
        self.report({'INFO'}, f"Quick preview rendered (step: {self.frame_step})")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_CleanupScene(Operator):
    """Clean up scene (remove unused data)"""
    bl_idname = "norent.cleanup_scene"
    bl_label = "Cleanup Scene"
    bl_description = "Remove unused materials, textures, and other data"
    
    def execute(self, context):
        # Store initial counts
        initial_materials = len(bpy.data.materials)
        initial_textures = len(bpy.data.textures)
        initial_images = len(bpy.data.images)
        
        # Remove unused data blocks
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        
        # Calculate cleaned items
        cleaned_materials = initial_materials - len(bpy.data.materials)
        cleaned_textures = initial_textures - len(bpy.data.textures)
        cleaned_images = initial_images - len(bpy.data.images)
        
        total_cleaned = cleaned_materials + cleaned_textures + cleaned_images
        
        if total_cleaned > 0:
            self.report({'INFO'}, f"Cleaned {total_cleaned} unused data blocks")
        else:
            self.report({'INFO'}, "Scene already clean")
        
        return {'FINISHED'}

class NORENT_OT_BatchRename(Operator):
    """Batch rename objects with NORENT prefix"""
    bl_idname = "norent.batch_rename"
    bl_label = "Batch Rename"
    bl_description = "Rename selected objects with NORENT naming convention"
    
    prefix: StringProperty(
        name="Prefix",
        description="Prefix for object names",
        default="NORENT_"
    )
    
    base_name: StringProperty(
        name="Base Name",
        description="Base name for objects",
        default="Object"
    )
    
    def execute(self, context):
        selected_objects = context.selected_objects
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for i, obj in enumerate(selected_objects, 1):
            obj.name = f"{self.prefix}{self.base_name}_{i:02d}"
        
        self.report({'INFO'}, f"Renamed {len(selected_objects)} objects")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_CreateBrandColors(Operator):
    """Create NORENT brand color palette"""
    bl_idname = "norent.create_brand_colors"
    bl_label = "Create Brand Colors"
    bl_description = "Create material palette with NORENT brand colors"
    
    def execute(self, context):
        # NORENT brand colors
        colors = {
            "NORENT_Black": (0.0, 0.0, 0.0, 1.0),
            "NORENT_White": (1.0, 1.0, 1.0, 1.0),
            "NORENT_Red": (0.8, 0.1, 0.1, 1.0),
            "NORENT_Orange": (1.0, 0.5, 0.0, 1.0),
            "NORENT_Yellow": (1.0, 0.9, 0.0, 1.0),
            "NORENT_Gray": (0.3, 0.3, 0.3, 1.0),
            "NORENT_DarkGray": (0.15, 0.15, 0.15, 1.0),
        }
        
        created_count = 0
        
        for name, color in colors.items():
            # Check if material already exists
            if name in bpy.data.materials:
                continue
                
            # Create material
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            
            # Set up nodes
            nodes = mat.node_tree.nodes
            principled = nodes.get("Principled BSDF")
            
            if principled:
                principled.inputs['Base Color'].default_value = color
                principled.inputs['Metallic'].default_value = 0.0
                principled.inputs['Roughness'].default_value = 0.5
            
            created_count += 1
        
        self.report({'INFO'}, f"Created {created_count} brand color materials")
        return {'FINISHED'}

class NORENT_OT_ProjectInfo(Operator):
    """Show project information and tips"""
    bl_idname = "norent.project_info"
    bl_label = "Project Info"
    bl_description = "Show current project information and workflow tips"
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Project info
        box = layout.box()
        box.label(text="PROJECT STATUS", icon='INFO')
        
        col = box.column(align=True)
        col.label(text=f"Scene: {scene.name}")
        col.label(text=f"Frame Range: {scene.frame_start} - {scene.frame_end}")
        col.label(text=f"Current Frame: {scene.frame_current}")
        col.label(text=f"FPS: {scene.render.fps}")
        
        # Render settings
        render = scene.render
        preset = scene.norent.render_preset
        col.label(text=f"Render Preset: {preset}")
        col.label(text=f"Resolution: {render.resolution_x}x{render.resolution_y}")
        
        # Object count
        obj_count = len(scene.objects)
        animated_count = len([obj for obj in scene.objects if obj.animation_data])
        col.label(text=f"Objects: {obj_count} ({animated_count} animated)")
        
        # Tips
        layout.separator()
        box = layout.box()
        box.label(text="WORKFLOW TIPS", icon='LIGHTBULB')
        
        tips = [
            "• Use Ctrl+A to apply transforms",
            "• Press Space for animation playback",
            "• Shift+A for quick object adding",
            "• Tab to enter edit mode",
            "• G, R, S for move, rotate, scale"
        ]
        
        for tip in tips:
            box.label(text=tip)

class NORENT_OT_ExportProject(Operator):
    """Export complete project package"""
    bl_idname = "norent.export_project"
    bl_label = "Export Project"
    bl_description = "Export complete project with all assets"
    
    include_renders: BoolProperty(
        name="Include Renders",
        description="Include rendered outputs in export",
        default=True
    )
    
    include_previews: BoolProperty(
        name="Include Previews",
        description="Include preview files in export",
        default=False
    )
    
    def execute(self, context):
        import shutil
        
        # Get project directory
        blend_path = bpy.data.filepath
        if not blend_path:
            self.report({'ERROR'}, "Save project file first")
            return {'CANCELLED'}
        
        project_dir = os.path.dirname(blend_path)
        project_name = os.path.splitext(os.path.basename(blend_path))[0]
        
        # Create export directory
        export_dir = os.path.join(project_dir, f"{project_name}_EXPORT")
        if os.path.exists(export_dir):
            shutil.rmtree(export_dir)
        os.makedirs(export_dir)
        
        # Copy main blend file
        shutil.copy2(blend_path, export_dir)
        
        # Copy NORENT directories if they exist
        norent_dirs = ["NORENT_Renders", "NORENT_Exports", "NORENT_Templates"]
        if self.include_previews:
            norent_dirs.append("NORENT_Previews")
        
        copied_dirs = 0
        for dir_name in norent_dirs:
            src_dir = os.path.join(project_dir, dir_name)
            if os.path.exists(src_dir):
                dst_dir = os.path.join(export_dir, dir_name)
                shutil.copytree(src_dir, dst_dir)
                copied_dirs += 1
        
        # Create project info file
        info_file = os.path.join(export_dir, "PROJECT_INFO.txt")
        with open(info_file, 'w') as f:
            f.write("NORENT MOTION PROJECT EXPORT\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Project Name: {project_name}\n")
            f.write(f"Export Date: {bpy.app.build_date}\n")
            f.write(f"Blender Version: {bpy.app.version_string}\n")
            f.write(f"NORENT Motion Version: 1.0.0\n\n")
            f.write("Contents:\n")
            f.write(f"- Main project file: {os.path.basename(blend_path)}\n")
            f.write(f"- Asset directories: {copied_dirs}\n\n")
            f.write("To use this project:\n")
            f.write("1. Open the .blend file in Blender\n")
            f.write("2. Install NORENT Motion add-on if not already installed\n")
            f.write("3. All assets should be properly linked\n")
        
        self.report({'INFO'}, f"Project exported to {export_dir}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Registration
classes = [
    NORENT_OT_RenderStill,
    NORENT_OT_RenderAnimation,
    NORENT_OT_ExportMP4,
    NORENT_OT_ExportGIF,
    NORENT_OT_LoadTemplate,
    NORENT_OT_SaveTemplate,
    NORENT_OT_OptimizeScene,
    NORENT_OT_QuickPreview,
    NORENT_OT_CleanupScene,
    NORENT_OT_BatchRename,
    NORENT_OT_CreateBrandColors,
    NORENT_OT_ProjectInfo,
    NORENT_OT_ExportProject,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)