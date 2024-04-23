import comfy_annotations

import transceiver.save_image_mem

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Import your module that defines nodes, so that ComfyFunc has a chance to process them.
# Actually add the @ComfyFunc nodes to what ComfyUI picks up.

NODE_CLASS_MAPPINGS.update(comfy_annotations.NODE_CLASS_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(comfy_annotations.NODE_DISPLAY_NAME_MAPPINGS)

# Set up any non-ComfyFunc node types as needed.
# NODE_CLASS_MAPPINGS.update(example.example_nodes.NODE_CLASS_MAPPINGS)
# NODE_DISPLAY_NAME_MAPPINGS.update(example.example_nodes.NODE_DISPLAY_NAME_MAPPINGS)

# Export so that ComfyUI can pick them up.
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
