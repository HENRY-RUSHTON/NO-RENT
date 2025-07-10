import bpy
import bmesh
from mathutils import Vector
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, IntProperty, EnumProperty

class NORENT_OT_TextAddAnimated(Operator):
    """Add animated text object with keyframes"""
    bl_idname = "norent.text_add_animated"
    bl_label = "Add Animated Text"
    bl_description = "Create text with basic animation"
    
    text_content: StringProperty(
        name="Text",
        description="Text content",
        default="NORENT"
    )
    
    def execute(self, context):
        # Create text object
        bpy.ops.object.text_add()
        text_obj = context.object
        text_obj.name = f"Text_{self.text_content}"
        text_obj.data.body = self.text_content
        
        # Set up text properties
        text_obj.data.size = 2.0
        text_obj.data.extrude = 0.1
        text_obj.data.bevel_depth = 0.02
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'
        
        # Add basic scale animation
        text_obj.scale = (0, 0, 0)
        text_obj.keyframe_insert(data_path="scale", frame=1)
        
        text_obj.scale = (1, 1, 1)
        text_obj.keyframe_insert(data_path="scale", frame=30)
        
        # Set easing
        self.set_ease_in_out(text_obj, "scale")
        
        self.report({'INFO'}, f"Added animated text: {self.text_content}")
        return {'FINISHED'}
    
    def set_ease_in_out(self, obj, data_path):
        """Apply ease in/out to keyframes"""
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                if data_path in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_TextAddTypewriter(Operator):
    """Add typewriter effect text"""
    bl_idname = "norent.text_add_typewriter"
    bl_label = "Add Typewriter Text"
    bl_description = "Create text with typewriter effect"
    
    text_content: StringProperty(
        name="Text",
        description="Text content",
        default="NORENT MOTION"
    )
    
    speed: FloatProperty(
        name="Speed",
        description="Characters per second",
        default=2.0,
        min=0.1,
        max=10.0
    )
    
    def execute(self, context):
        # Create text object
        bpy.ops.object.text_add()
        text_obj = context.object
        text_obj.name = f"Typewriter_{self.text_content[:10]}"
        text_obj.data.body = self.text_content
        
        # Set up text properties
        text_obj.data.size = 1.5
        text_obj.data.align_x = 'LEFT'
        text_obj.data.align_y = 'CENTER'
        
        # Create typewriter effect using text reveal
        self.create_typewriter_effect(text_obj, self.text_content, self.speed)
        
        self.report({'INFO'}, f"Added typewriter text: {self.text_content}")
        return {'FINISHED'}
    
    def create_typewriter_effect(self, text_obj, text, speed):
        """Create typewriter effect by animating text reveal"""
        chars_per_frame = speed / 30.0  # Convert to per-frame
        total_chars = len(text)
        
        # Animate text content character by character
        for i in range(total_chars + 1):
            frame = int(i / chars_per_frame) + 1
            revealed_text = text[:i]
            
            # Set text body
            text_obj.data.body = revealed_text
            text_obj.data.keyframe_insert(data_path="body", frame=frame)
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_TextAddBounce(Operator):
    """Add bounce-in text effect"""
    bl_idname = "norent.text_add_bounce"
    bl_label = "Add Bounce Text"
    bl_description = "Create text with bounce-in effect"
    
    text_content: StringProperty(
        name="Text",
        description="Text content",
        default="BOUNCE"
    )
    
    def execute(self, context):
        # Create text object
        bpy.ops.object.text_add()
        text_obj = context.object
        text_obj.name = f"Bounce_{self.text_content}"
        text_obj.data.body = self.text_content
        
        # Set up text properties
        text_obj.data.size = 2.5
        text_obj.data.extrude = 0.2
        text_obj.data.bevel_depth = 0.05
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'
        
        # Create bounce animation
        self.create_bounce_effect(text_obj)
        
        self.report({'INFO'}, f"Added bounce text: {self.text_content}")
        return {'FINISHED'}
    
    def create_bounce_effect(self, text_obj):
        """Create bounce effect with overshoot"""
        # Start small
        text_obj.scale = (0.1, 0.1, 0.1)
        text_obj.keyframe_insert(data_path="scale", frame=1)
        
        # Overshoot
        text_obj.scale = (1.2, 1.2, 1.2)
        text_obj.keyframe_insert(data_path="scale", frame=20)
        
        # Settle back
        text_obj.scale = (1.0, 1.0, 1.0)
        text_obj.keyframe_insert(data_path="scale", frame=35)
        
        # Apply custom easing for bounce
        if text_obj.animation_data and text_obj.animation_data.action:
            for fcurve in text_obj.animation_data.action.fcurves:
                if "scale" in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'FREE'
                        keyframe.handle_right_type = 'FREE'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_TextAddWipe(Operator):
    """Add wipe-up text effect"""
    bl_idname = "norent.text_add_wipe"
    bl_label = "Add Wipe Text"
    bl_description = "Create text with wipe-up reveal effect"
    
    text_content: StringProperty(
        name="Text",
        description="Text content",
        default="WIPE UP"
    )
    
    direction: EnumProperty(
        name="Direction",
        description="Wipe direction",
        items=[
            ('UP', "Up", "Wipe from bottom to top"),
            ('DOWN', "Down", "Wipe from top to bottom"),
            ('LEFT', "Left", "Wipe from right to left"),
            ('RIGHT', "Right", "Wipe from left to right")
        ],
        default='UP'
    )
    
    def execute(self, context):
        # Create text object
        bpy.ops.object.text_add()
        text_obj = context.object
        text_obj.name = f"Wipe_{self.text_content}"
        text_obj.data.body = self.text_content
        
        # Set up text properties
        text_obj.data.size = 2.0
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'
        
        # Create wipe effect using a plane as mask
        self.create_wipe_effect(text_obj, self.direction)
        
        self.report({'INFO'}, f"Added wipe text: {self.text_content}")
        return {'FINISHED'}
    
    def create_wipe_effect(self, text_obj, direction):
        """Create wipe effect using animated position"""
        # Start position based on direction
        if direction == 'UP':
            start_offset = Vector((0, -5, 0))
        elif direction == 'DOWN':
            start_offset = Vector((0, 5, 0))
        elif direction == 'LEFT':
            start_offset = Vector((5, 0, 0))
        else:  # RIGHT
            start_offset = Vector((-5, 0, 0))
        
        # Set initial position
        text_obj.location = text_obj.location + start_offset
        text_obj.keyframe_insert(data_path="location", frame=1)
        
        # End position (original location)
        text_obj.location = text_obj.location - start_offset
        text_obj.keyframe_insert(data_path="location", frame=45)
        
        # Add ease out
        if text_obj.animation_data and text_obj.animation_data.action:
            for fcurve in text_obj.animation_data.action.fcurves:
                if "location" in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'VECTOR'
                        keyframe.handle_right_type = 'AUTO'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_TextAnimateScale(Operator):
    """Animate selected text with scale effect"""
    bl_idname = "norent.text_animate_scale"
    bl_label = "Animate Scale"
    bl_description = "Add scale animation to selected text"
    
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'FONT':
            self.report({'ERROR'}, "Select a text object")
            return {'CANCELLED'}
        
        # Create material if it doesn't exist
        if not obj.data.materials:
            mat = bpy.data.materials.new(name=f"{obj.name}_Material")
            mat.use_nodes = True
            obj.data.materials.append(mat)
        
        material = obj.data.materials[0]
        
        # Set up material nodes for alpha animation
        if material.use_nodes:
            nodes = material.node_tree.nodes
            principled = nodes.get("Principled BSDF")
            if principled:
                current_frame = context.scene.frame_current
                
                # Fade in
                principled.inputs['Alpha'].default_value = 0.0
                principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=current_frame)
                
                principled.inputs['Alpha'].default_value = 1.0
                principled.inputs['Alpha'].keyframe_insert(data_path="default_value", frame=current_frame + 30)
                
                # Enable transparency
                material.blend_method = 'BLEND'
        
        self.report({'INFO'}, "Fade animation added")
        return {'FINISHED'}

class NORENT_OT_TextAnimateSlide(Operator):
    """Animate selected text with slide effect"""
    bl_idname = "norent.text_animate_slide"
    bl_label = "Animate Slide"
    bl_description = "Add slide animation to selected text"
    
    direction: EnumProperty(
        name="Direction",
        description="Slide direction",
        items=[
            ('LEFT', "From Left", "Slide in from left"),
            ('RIGHT', "From Right", "Slide in from right"),
            ('UP', "From Up", "Slide in from top"),
            ('DOWN', "From Down", "Slide in from bottom")
        ],
        default='LEFT'
    )
    
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'FONT':
            self.report({'ERROR'}, "Select a text object")
            return {'CANCELLED'}
        
        # Clear existing location keyframes
        if obj.animation_data:
            for fcurve in obj.animation_data.action.fcurves:
                if "location" in fcurve.data_path:
                    obj.animation_data.action.fcurves.remove(fcurve)
        
        current_frame = context.scene.frame_current
        current_location = obj.location.copy()
        
        # Set start position based on direction
        offset_distance = 10.0
        if self.direction == 'LEFT':
            start_location = current_location + Vector((-offset_distance, 0, 0))
        elif self.direction == 'RIGHT':
            start_location = current_location + Vector((offset_distance, 0, 0))
        elif self.direction == 'UP':
            start_location = current_location + Vector((0, offset_distance, 0))
        else:  # DOWN
            start_location = current_location + Vector((0, -offset_distance, 0))
        
        # Animate from start to current position
        obj.location = start_location
        obj.keyframe_insert(data_path="location", frame=current_frame)
        
        obj.location = current_location
        obj.keyframe_insert(data_path="location", frame=current_frame + 30)
        
        # Apply easing
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                if "location" in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'VECTOR'
                        keyframe.handle_right_type = 'AUTO'
        
        self.report({'INFO'}, f"Slide animation added ({self.direction})")
        return {'FINISHED'}

class NORENT_OT_TextAnimateWords(Operator):
    """Animate text word by word"""
    bl_idname = "norent.text_animate_words"
    bl_label = "Animate Words"
    bl_description = "Animate text appearing word by word"
    
    delay: FloatProperty(
        name="Word Delay",
        description="Delay between words (seconds)",
        default=0.3,
        min=0.1,
        max=2.0
    )
    
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'FONT':
            self.report({'ERROR'}, "Select a text object")
            return {'CANCELLED'}
        
        text_content = obj.data.body
        words = text_content.split()
        
        if len(words) <= 1:
            self.report({'WARNING'}, "Text needs multiple words for word animation")
            return {'CANCELLED'}
        
        # Clear existing keyframes
        obj.animation_data_clear()
        
        current_frame = context.scene.frame_current
        frames_per_word = int(self.delay * 30)  # Convert to frames
        
        # Animate text appearing word by word
        for i in range(len(words) + 1):
            frame = current_frame + (i * frames_per_word)
            partial_text = " ".join(words[:i])
            
            obj.data.body = partial_text
            obj.data.keyframe_insert(data_path="body", frame=frame)
        
        self.report({'INFO'}, f"Word-by-word animation added ({len(words)} words)")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_TextToParticles(Operator):
    """Convert text to particle system for advanced effects"""
    bl_idname = "norent.text_to_particles"
    bl_label = "Text to Particles"
    bl_description = "Convert text to particle system for advanced animations"
    
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'FONT':
            self.report({'ERROR'}, "Select a text object")
            return {'CANCELLED'}
        
        # Convert text to mesh
        bpy.ops.object.convert(target='MESH')
        
        # Add particle system
        bpy.ops.object.particle_system_add()
        particle_system = obj.particle_systems[0]
        settings = particle_system.settings
        
        # Configure particle system for text effects
        settings.type = 'EMITTER'
        settings.count = 100
        settings.emit_from = 'FACE'
        settings.use_emit_random = True
        settings.lifetime = 120
        settings.frame_start = context.scene.frame_current
        settings.frame_end = context.scene.frame_current + 60
        
        # Physics settings
        settings.physics_type = 'NEWTON'
        settings.mass = 0.1
        settings.particle_size = 0.05
        settings.size_random = 0.5
        
        # Force fields
        settings.effector_weights.gravity = 0.1
        
        self.report({'INFO'}, "Text converted to particle system")
        return {'FINISHED'}

# Registration
classes = [
    NORENT_OT_TextAddAnimated,
    NORENT_OT_TextAddTypewriter,
    NORENT_OT_TextAddBounce,
    NORENT_OT_TextAddWipe,
    NORENT_OT_TextAnimateScale,
    NORENT_OT_TextAnimateFade,
    NORENT_OT_TextAnimateSlide,
    NORENT_OT_TextAnimateWords,
    NORENT_OT_TextToParticles,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
        # Clear existing scale keyframes
        obj.animation_data_clear()
        
        # Add scale animation
        current_frame = context.scene.frame_current
        
        obj.scale = (0, 0, 0)
        obj.keyframe_insert(data_path="scale", frame=current_frame)
        
        obj.scale = (1, 1, 1)
        obj.keyframe_insert(data_path="scale", frame=current_frame + 30)
        
        self.report({'INFO'}, "Scale animation added")
        return {'FINISHED'}

class NORENT_OT_TextAnimateFade(Operator):
    """Animate selected text with fade effect"""
    bl_idname = "norent.text_animate_fade"
    bl_label = "Animate Fade"
    bl_description = "Add fade animation to selected text"
    
    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'FONT':
            self.report({'ERROR'}, "Select a text object")
            return {'CANCELLED'}
        