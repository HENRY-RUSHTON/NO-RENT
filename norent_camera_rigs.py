import bpy
import bmesh
from mathutils import Vector, Euler
from mathutils.noise import noise
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, EnumProperty, BoolProperty
import math

class NORENT_OT_CameraAddBasic(Operator):
    """Add basic camera rig with null controls"""
    bl_idname = "norent.camera_add_basic"
    bl_label = "Add Basic Camera Rig"
    bl_description = "Create camera with control empty for easy animation"
    
    def execute(self, context):
        # Create camera
        bpy.ops.object.camera_add()
        camera = context.object
        camera.name = "NORENT_Camera"
        
        # Position camera
        camera.location = (7, -7, 5)
        camera.rotation_euler = (1.1, 0, 0.785)
        
        # Create control empty
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        control_empty = context.object
        control_empty.name = "NORENT_Camera_Control"
        control_empty.empty_display_size = 2.0
        
        # Parent camera to control
        camera.parent = control_empty
        camera.parent_type = 'OBJECT'
        
        # Set as active camera
        context.scene.camera = camera
        
        # Add custom properties for easy animation
        control_empty["orbit_distance"] = 10.0
        control_empty["height"] = 5.0
        control_empty["target_x"] = 0.0
        control_empty["target_y"] = 0.0
        control_empty["target_z"] = 0.0
        
        self.report({'INFO'}, "Basic camera rig created")
        return {'FINISHED'}

class NORENT_OT_CameraAddHandheld(Operator):
    """Add handheld camera with shake"""
    bl_idname = "norent.camera_add_handheld"
    bl_label = "Add Handheld Camera"
    bl_description = "Create camera with built-in handheld shake"
    
    shake_strength: FloatProperty(
        name="Shake Strength",
        description="Intensity of camera shake",
        default=0.1,
        min=0.01,
        max=1.0
    )
    
    shake_speed: FloatProperty(
        name="Shake Speed",
        description="Speed of camera shake",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    def execute(self, context):
        # Create basic rig first
        bpy.ops.norent.camera_add_basic()
        camera = bpy.data.objects["NORENT_Camera"]
        
        # Rename for handheld
        camera.name = "NORENT_Handheld_Camera"
        
        # Add noise modifiers for shake
        self.add_handheld_shake(camera, self.shake_strength, self.shake_speed)
        
        self.report({'INFO'}, f"Handheld camera created (shake: {self.shake_strength})")
        return {'FINISHED'}
    
    def add_handheld_shake(self, camera, strength, speed):
        """Add noise-based shake to camera"""
        # Add noise modifier to location
        for i, axis in enumerate(['X', 'Y', 'Z']):
            # Create driver for each axis
            driver = camera.driver_add("location", i).driver
            driver.type = 'SCRIPTED'
            
            # Add noise expression
            noise_expr = f"noise(frame * {speed} * 0.1 + {i * 10}) * {strength}"
            driver.expression = noise_expr
            
            # Add frame variable
            var = driver.variables.new()
            var.name = "frame"
            var.type = 'SINGLE_PROP'
            var.targets[0].id = bpy.context.scene
            var.targets[0].data_path = "frame_current"
        
        # Add subtle rotation shake
        for i, axis in enumerate(['X', 'Y', 'Z']):
            driver = camera.driver_add("rotation_euler", i).driver
            driver.type = 'SCRIPTED'
            
            noise_expr = f"noise(frame * {speed} * 0.08 + {i * 15}) * {strength * 0.1}"
            driver.expression = noise_expr
            
            var = driver.variables.new()
            var.name = "frame"
            var.type = 'SINGLE_PROP'
            var.targets[0].id = bpy.context.scene
            var.targets[0].data_path = "frame_current"
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_CameraAddDolly(Operator):
    """Add camera dolly track"""
    bl_idname = "norent.camera_add_dolly"
    bl_label = "Add Dolly Track"
    bl_description = "Create camera on a curved dolly track"
    
    track_length: FloatProperty(
        name="Track Length",
        description="Length of dolly track",
        default=20.0,
        min=5.0,
        max=100.0
    )
    
    def execute(self, context):
        # Create curve for dolly track
        bpy.ops.curve.primitive_nurbs_path_add()
        curve = context.object
        curve.name = "NORENT_Dolly_Track"
        
        # Scale and position track
        curve.scale = (self.track_length / 2, self.track_length / 2, 1)
        curve.location = (0, 0, 2)
        
        # Create camera
        bpy.ops.object.camera_add()
        camera = context.object
        camera.name = "NORENT_Dolly_Camera"
        
        # Add follow path constraint
        constraint = camera.constraints.new(type='FOLLOW_PATH')
        constraint.target = curve
        constraint.use_curve_follow = True
        constraint.use_curve_radius = False
        
        # Add custom property for animation
        camera["dolly_position"] = 0.0
        
        # Create driver to control position
        driver = constraint.driver_add("offset_factor").driver
        driver.type = 'AVERAGE'
        
        var = driver.variables.new()
        var.name = "position"
        var.type = 'SINGLE_PROP'
        var.targets[0].id = camera
        var.targets[0].data_path = '["dolly_position"]'
        
        # Set as active camera
        context.scene.camera = camera
        
        self.report({'INFO'}, f"Dolly track created ({self.track_length}m)")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_CameraPushIn(Operator):
    """Add push-in camera move"""
    bl_idname = "norent.camera_push_in"
    bl_label = "Camera Push In"
    bl_description = "Animate camera pushing toward target"
    
    duration: IntProperty(
        name="Duration (frames)",
        description="Animation duration in frames",
        default=60,
        min=10,
        max=300
    )
    
    distance: FloatProperty(
        name="Push Distance",
        description="How far to push in",
        default=5.0,
        min=0.5,
        max=20.0
    )
    
    def execute(self, context):
        camera = context.scene.camera
        if not camera:
            self.report({'ERROR'}, "No active camera found")
            return {'CANCELLED'}
        
        current_frame = context.scene.frame_current
        start_location = camera.location.copy()
        
        # Calculate push direction (toward scene center)
        direction = Vector((0, 0, 0)) - start_location
        direction.normalize()
        end_location = start_location + (direction * self.distance)
        
        # Clear existing location keyframes
        camera.animation_data_clear()
        
        # Set keyframes
        camera.location = start_location
        camera.keyframe_insert(data_path="location", frame=current_frame)
        
        camera.location = end_location
        camera.keyframe_insert(data_path="location", frame=current_frame + self.duration)
        
        # Apply easing
        self.apply_ease_in_out(camera, "location")
        
        self.report({'INFO'}, f"Push-in animation added ({self.duration} frames)")
        return {'FINISHED'}
    
    def apply_ease_in_out(self, obj, data_path):
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

class NORENT_OT_CameraRotate(Operator):
    """Add orbit rotation around target"""
    bl_idname = "norent.camera_rotate"
    bl_label = "Camera Rotate Around"
    bl_description = "Animate camera orbiting around target"
    
    duration: IntProperty(
        name="Duration (frames)",
        description="Animation duration in frames",
        default=120,
        min=30,
        max=600
    )
    
    angle: FloatProperty(
        name="Rotation Angle",
        description="Angle to rotate in degrees",
        default=90.0,
        min=-360.0,
        max=360.0
    )
    
    axis: EnumProperty(
        name="Rotation Axis",
        description="Axis to rotate around",
        items=[
            ('Z', "Z (Up)", "Rotate around Z axis"),
            ('Y', "Y (Forward)", "Rotate around Y axis"),
            ('X', "X (Right)", "Rotate around X axis")
        ],
        default='Z'
    )
    
    def execute(self, context):
        camera = context.scene.camera
        if not camera:
            self.report({'ERROR'}, "No active camera found")
            return {'CANCELLED'}
        
        # Create empty at scene center for rotation pivot
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        pivot = context.object
        pivot.name = "NORENT_Camera_Pivot"
        
        # Parent camera to pivot (keep transforms)
        camera.parent = pivot
        camera.parent_type = 'OBJECT'
        
        current_frame = context.scene.frame_current
        angle_rad = math.radians(self.angle)
        
        # Get current rotation
        current_rotation = pivot.rotation_euler.copy()
        
        # Calculate end rotation based on axis
        end_rotation = current_rotation.copy()
        if self.axis == 'X':
            end_rotation.x += angle_rad
        elif self.axis == 'Y':
            end_rotation.y += angle_rad
        else:  # Z
            end_rotation.z += angle_rad
        
        # Clear existing rotation keyframes
        if pivot.animation_data:
            for fcurve in pivot.animation_data.action.fcurves:
                if "rotation" in fcurve.data_path:
                    pivot.animation_data.action.fcurves.remove(fcurve)
        
        # Set keyframes
        pivot.rotation_euler = current_rotation
        pivot.keyframe_insert(data_path="rotation_euler", frame=current_frame)
        
        pivot.rotation_euler = end_rotation
        pivot.keyframe_insert(data_path="rotation_euler", frame=current_frame + self.duration)
        
        # Apply easing
        self.apply_ease_in_out(pivot, "rotation_euler")
        
        self.report({'INFO'}, f"Orbit animation added ({self.angle}° around {self.axis})")
        return {'FINISHED'}
    
    def apply_ease_in_out(self, obj, data_path):
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

class NORENT_OT_CameraShake(Operator):
    """Add camera shake to existing camera"""
    bl_idname = "norent.camera_shake"
    bl_label = "Add Camera Shake"
    bl_description = "Add shake effect to selected camera"
    
    strength: FloatProperty(
        name="Shake Strength",
        description="Intensity of camera shake",
        default=0.2,
        min=0.01,
        max=2.0
    )
    
    speed: FloatProperty(
        name="Shake Speed",
        description="Speed of camera shake",
        default=2.0,
        min=0.1,
        max=10.0
    )
    
    duration: IntProperty(
        name="Duration (frames)",
        description="Duration of shake effect",
        default=60,
        min=10,
        max=300
    )
    
    def execute(self, context):
        camera = context.scene.camera
        if not camera:
            self.report({'ERROR'}, "No active camera found")
            return {'CANCELLED'}
        
        current_frame = context.scene.frame_current
        
        # Add shake using keyframes with noise
        self.add_shake_keyframes(camera, current_frame, self.duration, self.strength, self.speed)
        
        self.report({'INFO'}, f"Camera shake added ({self.duration} frames)")
        return {'FINISHED'}
    
    def add_shake_keyframes(self, camera, start_frame, duration, strength, speed):
        """Add shake keyframes using noise"""
        original_location = camera.location.copy()
        
        # Sample shake at regular intervals
        shake_samples = max(10, duration // 5)  # At least 10 samples
        
        for i in range(shake_samples + 1):
            frame = start_frame + (i * duration // shake_samples)
            
            # Generate noise offset
            noise_x = (noise(Vector((frame * speed * 0.1, 0, 0))) - 0.5) * strength
            noise_y = (noise(Vector((0, frame * speed * 0.1, 0))) - 0.5) * strength
            noise_z = (noise(Vector((0, 0, frame * speed * 0.1))) - 0.5) * strength * 0.5
            
            shake_offset = Vector((noise_x, noise_y, noise_z))
            camera.location = original_location + shake_offset
            camera.keyframe_insert(data_path="location", frame=frame)
        
        # Return to original position
        camera.location = original_location
        camera.keyframe_insert(data_path="location", frame=start_frame + duration)
        
        # Set interpolation to linear for shake effect
        if camera.animation_data and camera.animation_data.action:
            for fcurve in camera.animation_data.action.fcurves:
                if "location" in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        if keyframe.co.x >= start_frame and keyframe.co.x <= start_frame + duration:
                            keyframe.interpolation = 'LINEAR'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NORENT_OT_CameraFocusPull(Operator):
    """Add focus pull effect"""
    bl_idname = "norent.camera_focus_pull"
    bl_label = "Camera Focus Pull"
    bl_description = "Animate camera depth of field focus"
    
    start_distance: FloatProperty(
        name="Start Focus Distance",
        description="Initial focus distance",
        default=5.0,
        min=0.1,
        max=100.0
    )
    
    end_distance: FloatProperty(
        name="End Focus Distance",
        description="Final focus distance",
        default=15.0,
        min=0.1,
        max=100.0
    )
    
    duration: IntProperty(
        name="Duration (frames)",
        description="Animation duration in frames",
        default=90,
        min=10,
        max=300
    )
    
    def execute(self, context):
        camera = context.scene.camera
        if not camera or camera.type != 'CAMERA':
            self.report({'ERROR'}, "No camera selected")
            return {'CANCELLED'}
        
        camera_data = camera.data
        
        # Enable depth of field
        camera_data.dof.use_dof = True
        camera_data.dof.aperture_fstop = 2.8
        
        current_frame = context.scene.frame_current
        
        # Clear existing focus keyframes
        if camera_data.animation_data:
            for fcurve in camera_data.animation_data.action.fcurves:
                if "focus_distance" in fcurve.data_path:
                    camera_data.animation_data.action.fcurves.remove(fcurve)
        
        # Set focus keyframes
        camera_data.dof.focus_distance = self.start_distance
        camera_data.dof.keyframe_insert(data_path="focus_distance", frame=current_frame)
        
        camera_data.dof.focus_distance = self.end_distance
        camera_data.dof.keyframe_insert(data_path="focus_distance", frame=current_frame + self.duration)
        
        # Apply smooth easing
        if camera_data.animation_data and camera_data.animation_data.action:
            for fcurve in camera_data.animation_data.action.fcurves:
                if "focus_distance" in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
        
        self.report({'INFO'}, f"Focus pull added ({self.start_distance}m → {self.end_distance}m)")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Registration
classes = [
    NORENT_OT_CameraAddBasic,
    NORENT_OT_CameraAddHandheld,
    NORENT_OT_CameraAddDolly,
    NORENT_OT_CameraPushIn,
    NORENT_OT_CameraRotate,
    NORENT_OT_CameraShake,
    NORENT_OT_CameraFocusPull,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)