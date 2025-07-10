# NORENT Motion - Blender Motion Graphics Add-on

> **Creative weapon disguised as motion graphics tools**

NORENT Motion transforms Blender into a motion graphics powerhouse with After Effects-inspired workflows, built for creators who refuse to rent their tools.

## 🎯 Features

### ✅ Layer-Like Panel (Timeline Abstraction)
- Group objects into "virtual layers"
- AE-style stacked interface with Solo/Mute/Visibility toggles
- Auto-naming and reordering in UI
- **Tech:** `bpy.types.UIList` + custom `bpy.types.Panel`

### ✅ Text Animator Presets
- **Bounce In:** Scale animation with overshoot
- **Typewriter:** Character-by-character reveal
- **Wipe Effects:** Directional text reveals
- **Scale Pop:** Dynamic scale animations
- **Word Animation:** Word-by-word reveals
- **Tech:** `bpy.ops.object.text_add()` + keyframe automation

### ✅ Easing Presets
- Ease In, Ease Out, Ease In-Out
- Overshoot, Bounce, Elastic effects
- Smart easing (auto-detects animation type)
- Copy easing between objects
- **Tech:** F-curve manipulation with custom bezier handles

### ✅ Camera Rig Presets
- **Basic Rig:** Camera + control empty setup
- **Handheld:** Noise-based shake system
- **Dolly Track:** Curve-based camera moves
- **Push In/Rotate:** Automated camera movements
- **Focus Pull:** Depth of field animation
- **Tech:** Parenting + drivers + noise modifiers

### ✅ Render & Export Tools
- **Render Presets:** Instagram Reel, Square, Story, Landscape
- **Export Formats:** MP4, GIF (frame export)
- **Quick Preview:** Fast viewport renders
- **Batch Tools:** Project export and cleanup

### ✅ Template System
- Lower thirds, lyric videos, intro splashes
- Save/load custom templates
- Asset management and organization
- **Tech:** `bpy.ops.wm.append()` from template library

## 🚀 Installation

### Requirements
- Blender 3.0+
- Python 3.7+

### Install Steps
1. Download `norent_motion.zip`
2. Open Blender → Edit → Preferences → Add-ons
3. Click "Install..." and select the ZIP file
4. Enable "NORENT Motion" in the add-ons list
5. Find the NORENT tab in 3D Viewport sidebar
6. Click "Setup Workspace" to configure Blender

## 📁 File Structure

```
norrent_motion/
├── __init__.py           # Main add-on file with registration
├── panel_ui.py          # UI panels and layer management
├── text_fx.py           # Text animation operators
├── camera_rigs.py       # Camera rig creation and animation
├── easing.py            # Keyframe easing presets
├── utils.py             # Render, export, and utility tools
├── templates/           # Animation templates
│   ├── lower_third.blend
│   ├── lyric_video.blend
│   └── intro_splash.blend
└── README.md           # This file
```

## 🎮 Quick Start

### 1. Setup Workspace
```python
# Click "Setup Workspace" or run:
bpy.ops.norent.setup_workspace()
```

### 2. Create Animated Text
```python
# Add bounce text
bpy.ops.norent.text_add_bounce(text_content="NORENT")

# Add typewriter effect
bpy.ops.norent.text_add_typewriter(text_content="MOTION GRAPHICS", speed=2.0)
```

### 3. Apply Easing
```python
# Select animated objects and apply easing
bpy.ops.norent.apply_easing(easing_type='OVERSHOOT', strength=1.5)

# Or use quick presets
bpy.ops.norent.ease_bounce()
bpy.ops.norent.smart_easing()  # Auto-detects best easing
```

### 4. Setup Camera
```python
# Create handheld camera
bpy.ops.norent.camera_add_handheld(shake_strength=0.2, shake_speed=2.0)

# Add camera movement
bpy.ops.norent.camera_push_in(duration=90, distance=5.0)
```

### 5. Render Export
```python
# Set render preset
bpy.context.scene.norent.render_preset = 'REEL'  # 1080x1920

# Render animation
bpy.ops.norent.render_animation()

# Export MP4
bpy.ops.norent.export_mp4()
```

## 🎨 Workflow Examples

### Creating a Lyric Video
1. Load lyric template: `bpy.ops.norent.load_template(template_name='LYRIC_VIDEO')`
2. Add typewriter text: `bpy.ops.norent.text_add_typewriter()`
3. Apply word animation: `bpy.ops.norent.text_animate_words(delay=0.5)`
4. Set camera: `bpy.ops.norent.camera_add_basic()`
5. Render: `bpy.ops.norent.export_mp4()`

### Instagram Reel Creation
1. Set preset: `scene.norent.render_preset = 'REEL'`
2. Add bounce text: `bpy.ops.norent.text_add_bounce(text_content="YOUR BRAND")`
3. Apply overshoot easing: `bpy.ops.norent.ease_overshoot()`
4. Add handheld camera: `bpy.ops.norent.camera_add_handheld()`
5. Quick render: `bpy.ops.norent.quick_preview(frame_step='2')`

## 🛠 Development

### Adding Custom Text Effects
```python
class NORENT_OT_TextAddCustom(Operator):
    bl_idname = "norent.text_add_custom"
    bl_label = "Add Custom Text"
    
    def execute(self, context):
        bpy.ops.object.text_add()
        text_obj = context.object
        
        # Add your custom animation here
        text_obj.scale = (0, 0, 0)
        text_obj.keyframe_insert(data_path="scale", frame=1)
        
        return {'FINISHED'}
```

### Adding Camera Rigs
```python
class NORENT_OT_CameraAddCustom(Operator):
    bl_idname = "norent.camera_add_custom"
    bl_label = "Add Custom Camera"
    
    def execute(self, context):
        bpy.ops.object.camera_add()
        camera = context.object
        
        # Add your custom camera setup here
        
        return {'FINISHED'}
```

## 🔧 Advanced Usage

### Layer Management
```python
# Access layer stack
scene = bpy.context.scene
active_layer = scene.norent.active_layer

# Add layer programmatically
bpy.ops.norent.layer_add()

# Batch rename objects
bpy.ops.norent.batch_rename(prefix="NORENT_", base_name="Element")
```

### Custom Easing Curves
```python
# Apply custom easing to F-curve
def apply_custom_easing(fcurve):
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'BEZIER'
        keyframe.handle_left_type = 'FREE'
        keyframe.handle_right_type = 'FREE'
        # Set custom handle positions
```

### Template Creation
```python
# Save current scene as template
bpy.ops.norent.save_template(template_name="My_Custom_Template")

# Load template
bpy.ops.norent.load_template(template_name="My_Custom_Template")
```

## 🎯 Pro Features

### Batch Operations
- Bulk text animation application
- Multi-object easing synchronization
- Batch export with different presets
- Project packaging and export

### Advanced Camera Tools
- Multi-camera setups
- Camera switching animations
- Complex dolly track systems
- Focus pulling automation

### Template Library
- Professional template collection
- Custom template creation tools
- Asset library management
- Version control for templates

## 🚨 Troubleshooting

### Common Issues

**Add-on not showing up:**
- Ensure Blender 3.0+
- Check Python console for errors
- Verify ZIP file extraction

**Animations not working:**
- Check timeline range (frame_start, frame_end)
- Verify object selection
- Enable auto-keyframe in timeline

**Render issues:**
- Check output path permissions
- Verify render settings
- Monitor system resources

**Template loading fails:**
- Check template file exists
- Verify file permissions
- Clear Blender cache

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check add-on status
addon_utils.check("norent_motion")
```

## 🤝 Contributing

### Development Setup
1. Clone repository
2. Link to Blender add-ons directory
3. Enable developer mode in Blender
4. Test with provided templates

### Adding Features
1. Follow existing code structure
2. Add operators to appropriate modules
3. Register in `__init__.py`
4. Update UI panels if needed
5. Add documentation

### Submitting Changes
1. Fork repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request
5. Update documentation

## 📝 License

**NORENT Motion** is released under the GPL v3 License.

**Creative freedom through ownership. No subscriptions. No surveillance. No surrender.**

---

## 🔗 Links

- **Website:** [norent.tools/motion](https://norent.tools/motion)
- **Documentation:** [docs.norent.tools](https://docs.norent.tools)
- **Community:** [discord.gg/norent](https://discord.gg/norent)
- **Support:** [motion@norent.tools](mailto:motion@norent.tools)

---

*Built by creators, for creators. Escape the subscription trap.*