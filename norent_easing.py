import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, FloatProperty
import bmesh
from mathutils import Vector

class NORENT_OT_ApplyEasing(Operator):
    """Apply easing preset to selected keyframes"""
    bl_idname = "norent.apply_easing"
    bl_label = "Apply Easing"
    bl_description = "Apply easing curve to selected keyframes"
    
    easing_type: EnumProperty(
        name="Easing Type",
        description="Type of easing to apply",
        items=[
            ('EASE_IN', "Ease In", "Slow start, fast end"),
            ('EASE_OUT', "Ease Out", "Fast start, slow end"),
            ('EASE_IN_OUT', "Ease In-Out", "Slow start and end"),
            ('OVERSHOOT', "Overshoot", "Bounce past target"),
            ('ANTICIPATE', "Anticipate", "Pull back before moving"),
            ('BOUNCE', "Bounce", "Elastic bounce effect"),
            ('ELASTIC', "Elastic", "Spring-like motion"),
            ('BACK', "Back", "Slight reverse before forward"),
            ('CUSTOM', "Custom", "Custom bezier handles")
        ],
        default='EASE_IN_OUT'
    )
    
    strength: FloatProperty(
        name="Strength",
        description="Strength of the easing effect",
        default=1.0,
        min=0.1,
        max=3.0
    )
    
    def execute(self, context):
        # Get selected objects with animation data
        animated_objects = [obj for obj in context.selected_objects if obj.animation_data]
        
        if not animated_objects:
            self.report({'WARNING'}, "No animated objects selected")
            return {'CANCELLED'}
        
        applied_count = 0
        
        for obj in animated_objects:
            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    if self.apply_easing_to_fcurve(fcurve, self.easing_type, self.strength):
                        applied_count += 1
        
        if applied_count > 0:
            self.report({'INFO'}, f"Applied {self.easing_type} easing to {applied_count} curves")
        else:
            self.report({'WARNING'}, "No keyframes found to apply easing")
        
        return {'FINISHED'}
    
    def apply_easing_to_fcurve(self, fcurve, easing_type, strength):
        """Apply easing to an F-curve"""
        keyframes = fcurve.keyframe_points
        if len(keyframes) < 2:
            return False
        
        for keyframe in keyframes:
            keyframe.interpolation = 'BEZIER'
            
            if easing_type == 'EASE_IN':
                keyframe.handle_left_type = 'VECTOR'
                keyframe.handle_right_type = 'AUTO'
                self.adjust_handle_strength(keyframe, 'right', strength)
                
            elif easing_type == 'EASE_OUT':
                keyframe.handle_left_type = 'AUTO'
                keyframe.handle_right_type = 'VECTOR'
                self.adjust_handle_strength(keyframe, 'left', strength)
                
            elif easing_type == 'EASE_IN_OUT':
                keyframe.handle_left_type = 'AUTO'
                keyframe.handle_right_type = 'AUTO'
                self.adjust_handle_strength(keyframe, 'both', strength)
                
            elif easing_type == 'OVERSHOOT':
                keyframe.handle_left_type = 'FREE'
                keyframe.handle_right_type = 'FREE'
                self.create_overshoot_handles(keyframe, strength)
                
            elif easing_type == 'ANTICIPATE':
                keyframe.handle_left_type = 'FREE'
                keyframe.handle_right_type = 'FREE'
                self.create_anticipate_handles(keyframe, strength)
                
            elif easing_type == 'BOUNCE':
                keyframe.handle_left_type = 'FREE'
                keyframe.handle_right_type = 'FREE'
                self.create_bounce_handles(keyframe, strength)
                
            elif easing_type == 'ELASTIC':
                keyframe.handle_left_type = 'FREE'
                keyframe.handle_right_type = 'FREE'
                self.create_elastic_handles(keyframe, strength)
                
            elif easing_type == 'BACK':
                keyframe.handle_left_type = 'FREE'
                keyframe.handle_right_type = 'FREE'
                self.create_back_handles(keyframe, strength)
        
        return True
    
    def adjust_handle_strength(self, keyframe, side, strength):
        """Adjust bezier handle strength"""
        if side in ['left', 'both']:
            handle = keyframe.handle_left
            co = keyframe.co
            direction = (handle - co).normalized()
            new_handle = co + direction * strength * 0.5
            keyframe.handle_left = new_handle
            
        if side in ['right', 'both']:
            handle = keyframe.handle_right
            co = keyframe.co
            direction = (handle - co).normalized()
            new_handle = co + direction * strength * 0.5
            keyframe.handle_right = new_handle
    
    def create_overshoot_handles(self, keyframe, strength):
        """Create overshoot effect handles"""
        co = keyframe.co
        offset = strength * 0.3
        
        # Left handle pulls back
        keyframe.handle_left = Vector((co.x - offset, co.y - offset * 0.5))
        # Right handle overshoots
        keyframe.handle_right = Vector((co.x + offset, co.y + offset * 0.5))
    
    def create_anticipate_handles(self, keyframe, strength):
        """Create anticipation effect handles"""
        co = keyframe.co
        offset = strength * 0.4
        
        # Both handles create anticipation curve
        keyframe.handle_left = Vector((co.x - offset, co.y + offset * 0.3))
        keyframe.handle_right = Vector((co.x + offset, co.y - offset * 0.3))
    
    def create_bounce_handles(self, keyframe, strength):
        """Create bounce effect handles"""
        co = keyframe.co
        offset = strength * 0.5
        
        # Handles create bouncy curve
        keyframe.handle_left = Vector((co.x - offset * 0.7, co.y - offset))
        keyframe.handle_right = Vector((co.x + offset * 0.7, co.y + offset))
    
    def create_elastic_handles(self, keyframe, strength):
        """Create elastic spring effect handles"""
        co = keyframe.co
        offset = strength * 0.6
        
        # Elastic curve with oscillation
        keyframe.handle_left = Vector((co.x - offset, co.y + offset * 0.8))
        keyframe.handle_right = Vector((co.x + offset, co.y - offset * 0.8))
    
    def create_back_handles(self, keyframe, strength):
        """Create back easing handles"""
        co = keyframe.co
        offset = strength * 0.3
        
        # Back curve - slight reverse motion
        keyframe.handle_left = Vector((co.x - offset * 0.5, co.y - offset))
        keyframe.handle_right = Vector((co.x + offset * 0.5, co.y + offset))

class NORENT_OT_EaseIn(Operator):
    """Quick ease in application"""
    bl_idname = "norent.ease_in"
    bl_label = "Ease In"
    bl_description = "Apply ease in to selected keyframes"
    
    def execute(self, context):
        bpy.ops.norent.apply_easing(easing_type='EASE_IN')
        return {'FINISHED'}

class NORENT_OT_EaseOut(Operator):
    """Quick ease out application"""
    bl_idname = "norent.ease_out"
    bl_label = "Ease Out"
    bl_description = "Apply ease out to selected keyframes"
    
    def execute(self, context):
        bpy.ops.norent.apply_easing(easing_type='EASE_OUT')
        return {'FINISHED'}

class NORENT_OT_EaseInOut(Operator):
    """Quick ease in-out application"""
    bl_idname = "norent.ease_in_out"
    bl_label = "Ease In-Out"
    bl_description = "Apply ease in-out to selected keyframes"
    
    def execute(self, context):
        bpy.ops.norent.apply_easing(easing_type='EASE_IN_OUT')
        return {'FINISHED'}

class NORENT_OT_EaseOvershoot(Operator):
    """Quick overshoot application"""
    bl_idname = "norent.ease_overshoot"
    bl_label = "Overshoot"
    bl_description = "Apply overshoot easing to selected keyframes"
    
    def execute(self, context):
        bpy.ops.norent.apply_easing(easing_type='OVERSHOOT')
        return {'FINISHED'}

class NORENT_OT_EaseBounce(Operator):
    """Quick bounce application"""
    bl_idname = "norent.ease_bounce"
    bl_label = "Bounce"
    bl_description = "Apply bounce easing to selected keyframes"
    
    def execute(self, context):
        bpy.ops.norent.apply_easing(easing_type='BOUNCE')
        return {'FINISHED'}

class NORENT_OT_EaseElastic(Operator):
    """Quick elastic application"""
    bl_idname = "norent.ease_elastic"
    bl_label = "Elastic"
    bl_description = "Apply elastic easing to selected keyframes"
    
    def execute(self, context):
        bpy.ops.norent.apply_easing(easing_type='ELASTIC')
        return {'FINISHED'}

class NORENT_OT_CopyEasing(Operator):
    """Copy easing from active to selected"""
    bl_idname = "norent.copy_easing"
    bl_label = "Copy Easing"
    bl_description = "Copy easing curve from active object to selected objects"
    
    def execute(self, context):
        active_obj = context.active_object
        selected_objs = [obj for obj in context.selected_objects if obj != active_obj]
        
        if not active_obj or not active_obj.animation_data:
            self.report({'ERROR'}, "Active object has no animation data")
            return {'CANCELLED'}
        
        if not selected_objs:
            self.report({'WARNING'}, "No other objects selected")
            return {'CANCELLED'}
        
        # Get easing data from active object
        active_action = active_obj.animation_data.action
        if not active_action:
            self.report({'ERROR'}, "Active object has no action")
            return {'CANCELLED'}
        
        copied_count = 0
        
        for target_obj in selected_objs:
            if not target_obj.animation_data or not target_obj.animation_data.action:
                continue
                
            target_action = target_obj.animation_data.action
            
            # Copy easing from matching f-curves
            for active_fcurve in active_action.fcurves:
                for target_fcurve in target_action.fcurves:
                    if (active_fcurve.data_path == target_fcurve.data_path and 
                        active_fcurve.array_index == target_fcurve.array_index):
                        
                        # Copy handle types and positions
                        for i, keyframe in enumerate(target_fcurve.keyframe_points):
                            if i < len(active_fcurve.keyframe_points):
                                active_key = active_fcurve.keyframe_points[i]
                                
                                keyframe.interpolation = active_key.interpolation
                                keyframe.handle_left_type = active_key.handle_left_type
                                keyframe.handle_right_type = active_key.handle_right_type
                                
                                # Copy handle positions (adjusted for different values)
                                if active_key.handle_left_type == 'FREE':
                                    ratio_left = (active_key.handle_left - active_key.co)
                                    keyframe.handle_left = keyframe.co + ratio_left
                                    
                                if active_key.handle_right_type == 'FREE':
                                    ratio_right = (active_key.handle_right - active_key.co)
                                    keyframe.handle_right = keyframe.co + ratio_right
                        
                        copied_count += 1
        
        self.report({'INFO'}, f"Copied easing to {copied_count} curves")
        return {'FINISHED'}

class NORENT_OT_ResetEasing(Operator):
    """Reset easing to linear"""
    bl_idname = "norent.reset_easing"
    bl_label = "Reset Easing"
    bl_description = "Reset all keyframes to linear interpolation"
    
    def execute(self, context):
        reset_count = 0
        
        for obj in context.selected_objects:
            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'LINEAR'
                        keyframe.handle_left_type = 'VECTOR'
                        keyframe.handle_right_type = 'VECTOR'
                    reset_count += 1
        
        self.report({'INFO'}, f"Reset {reset_count} curves to linear")
        return {'FINISHED'}

class NORENT_OT_SmartEasing(Operator):
    """Automatically apply appropriate easing based on animation type"""
    bl_idname = "norent.smart_easing"
    bl_label = "Smart Easing"
    bl_description = "Automatically choose best easing for animation type"
    
    def execute(self, context):
        applied_count = 0
        
        for obj in context.selected_objects:
            if not obj.animation_data or not obj.animation_data.action:
                continue
                
            for fcurve in obj.animation_data.action.fcurves:
                easing_type = self.determine_smart_easing(fcurve)
                if self.apply_smart_easing(fcurve, easing_type):
                    applied_count += 1
        
        self.report({'INFO'}, f"Applied smart easing to {applied_count} curves")
        return {'FINISHED'}
    
    def determine_smart_easing(self, fcurve):
        """Determine appropriate easing based on curve characteristics"""
        data_path = fcurve.data_path
        
        # Scale animations get bounce/overshoot
        if "scale" in data_path:
            return 'OVERSHOOT'
        
        # Location animations get ease in-out
        elif "location" in data_path:
            return 'EASE_IN_OUT'
        
        # Rotation animations get ease in-out
        elif "rotation" in data_path:
            return 'EASE_IN_OUT'
        
        # Alpha/transparency gets ease in or out
        elif "alpha" in data_path or "factor" in data_path:
            # Check if going from 0 to 1 or 1 to 0
            keyframes = fcurve.keyframe_points
            if len(keyframes) >= 2:
                start_val = keyframes[0].co.y
                end_val = keyframes[-1].co.y
                if start_val < end_val:
                    return 'EASE_OUT'  # Fade in
                else:
                    return 'EASE_IN'   # Fade out
        
        # Default to ease in-out
        return 'EASE_IN_OUT'
    
    def apply_smart_easing(self, fcurve, easing_type):
        """Apply determined easing to fcurve"""
        keyframes = fcurve.keyframe_points
        if len(keyframes) < 2:
            return False
        
        for keyframe in keyframes:
            keyframe.interpolation = 'BEZIER'
            
            if easing_type == 'EASE_IN':
                keyframe.handle_left_type = 'VECTOR'
                keyframe.handle_right_type = 'AUTO'
            elif easing_type == 'EASE_OUT':
                keyframe.handle_left_type = 'AUTO'
                keyframe.handle_right_type = 'VECTOR'
            elif easing_type == 'EASE_IN_OUT':
                keyframe.handle_left_type = 'AUTO'
                keyframe.handle_right_type = 'AUTO'
            elif easing_type == 'OVERSHOOT':
                keyframe.handle_left_type = 'FREE'
                keyframe.handle_right_type = 'FREE'
                # Create overshoot handles
                co = keyframe.co
                keyframe.handle_left = Vector((co.x - 0.3, co.y - 0.15))
                keyframe.handle_right = Vector((co.x + 0.3, co.y + 0.15))
        
        return True

# Registration
classes = [
    NORENT_OT_ApplyEasing,
    NORENT_OT_EaseIn,
    NORENT_OT_EaseOut,
    NORENT_OT_EaseInOut,
    NORENT_OT_EaseOvershoot,
    NORENT_OT_EaseBounce,
    NORENT_OT_EaseElastic,
    NORENT_OT_CopyEasing,
    NORENT_OT_ResetEasing,
    NORENT_OT_SmartEasing,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)