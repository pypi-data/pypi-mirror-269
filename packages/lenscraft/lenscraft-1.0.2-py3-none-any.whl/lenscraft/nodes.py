import pickle
from pathlib import Path
from importlib import resources
from typing import Dict, List, Optional
import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from lenscraft.gabor import gabor_features, Gabor

from lenscraft.image import DynamicTexture, Image, ImageLibrary
from lenscraft.texture import TextureModelLibrary
from lenscraft.utils import debounce

class Graph:
    def __init__(self, library: ImageLibrary):
        self.nodes: Dict[any, Node] = {}
        self.links: Dict[any, Link] = {}
        self.inputs: Dict[any, "NodeInput"] = {}
        self.outputs: Dict[any, "NodeOutput"] = {}

        #self.image_node = ImageLibraryNode(library)
        #self.nodes[self.image_node.id] = self.image_node

    def add_node(self, node):
        print("Add Node")
        self.nodes[node.id] = node

    def add_link(self, link):
        print("Link")
        self.links[link.id] = link
        link.connect()

    def delink(self, link_id):
        print("Delink")
        link = self.links.pop(link_id)
        link.disconnect()

    def get_input(self, id):
        for node in self.nodes.values():
            for input in node.inputs:
                if input.id == id:
                    return input

        raise ValueError("No such input")
    
    def get_output(self, id):
        for node in self.nodes.values():
            for output in node.outputs:
                if output.id == id:
                    return output

        raise ValueError("No such output")

class Link:
    def __init__(self, a1, a2):
        self.output = a1
        self.input = a2
        self.id = dpg.generate_uuid()

    def disconnect(self):
        self.output.delink(self.input)

    def connect(self):
        self.output.link(self.input)
class Node:
    def __init__(self):
        self.id = dpg.generate_uuid()

    def compute(self):
        pass

    def draw_config(self):
        pass

    def add_to_editor(self, parent=0, pos=(0,0)):
        with dpg.node(label=self.name, parent=parent, pos=pos, tag=self.id):
            self.draw_config()
            for input in self.inputs:
                input.draw()
            for output in self.outputs:
                output.draw()

    def get_input_value(self, name):
        for input in self.inputs:
            if input.name == name:
                return input.value

        raise ValueError(f"No such input: {name}")

    def set_output_value(self, name, value):
        for output in self.outputs:
            if output.name == name:
                output.set_value(value)
                return

        raise ValueError(f"No such output: {name}")
    
    def input_attribute(self, id):
        for a in self.inputs:
            if a.id == id:
                return a
            
        raise ValueError("No such input attribute")
    
    def output_attribute(self, id):
        for a in self.outputs:
            if a.id == id:
                return a
            
        raise ValueError("No such output attribute")


class NodeInput:
    def __init__(self, name, node: Node):
        self.name = name
        self.id = dpg.generate_uuid()
        self.value = None
        self.parent_node = node


    def update_value(self, new_value):
        self.value = new_value
        self.parent_node.compute()

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_text(self.name)


class IntNodeInput(NodeInput):
    def __init__(self, name, node: Node):
        super().__init__(name, node)
        self.value = 12

    def _callback(self, sender, app_data):
        self.update_value(app_data)

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_input_int(
                label=self.name,
                default_value=self.value,
                width=100,
                callback=self._callback,
            )


class NumberSliderAttribute(NodeInput):
    def __init__(self, name, node, max_value=100, min_value=0, initial_value=50):
        super().__init__(name, node)
        self.max_value = max_value
        self.min_value = min_value
        self.initial_value = initial_value
        self.value = initial_value

    def _callback(self, sender, app_data):
        self.update_value(app_data)

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_slider_int(
                label=self.name,
                max_value=self.max_value,
                min_value=self.min_value,
                default_value=self.initial_value,
                width=200,
                callback=self._callback,
            )


class ImageNodeInput(NodeInput):
    def __init__(self, name, node):
        super().__init__(name, node)

    def draw(self):
        with dpg.node_attribute(label=self.id, attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_text("Image")



class NodeOutput:
    outputs: Dict[any, "NodeOutput"] = {}

    def __init__(self, name, node:Node):
        self.name = name
        self.id = dpg.generate_uuid()
        self.downstream: List[NodeInput] = []
        self.value = None

    def link(self, input: NodeInput):
        self.downstream.append(input)
        if self.value is not None:
            input.update_value(self.value)

    def delink(self, input: NodeInput):
        self.downstream.remove(input)

    def set_value(self, new_value):
        self.value = new_value
        for d in self.downstream:
            d.update_value(new_value)

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=self.id):
            dpg.add_text(default_value=self.name)


class ImageNodeOutput(NodeOutput):
    def __init__(self, name, node):
        super().__init__(name, node)

        self.preview = None
        self.texture = None

    def draw(self):
        with dpg.node_attribute(
            attribute_type=dpg.mvNode_Attr_Output, tag=self.id
        ) as attr:
            dpg.add_text(self.name)
            self.preview_container = attr

    def set_value(self, new_value):
        super().set_value(new_value)

        if self.texture is None:
            self.texture = DynamicTexture(new_value)
        else:
            self.texture.update(new_value)

        if self.preview:
            dpg.delete_item(self.preview)
        self.preview = self.texture.add_to_parent(self.preview_container, width=200)


class ImageLibraryNode(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Image Library"
        self.inputs = []
        self.outputs = [ImageLibraryAttribute("Image", self, context.library)]

class ObjectSVMNode(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Find Texture"
        self.inputs = [ImageNodeInput("Image", self)]
        self.outputs = [ImageNodeOutput("Result", self)]

        self.texture_select = TextureLibraryAttribute("Texture Model", self, context.texture_library)
        self.texture_select.add_callback(self._on_select)

    def compute(self):
        image = self.get_input_value("Image")
        print("Image shape", image.shape)
        h, w = image.shape[0:2]
        gabor = Gabor()
        features = gabor.generate_features(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        fv = features.all()
        result = self.model.predict(fv).reshape((h, w))
        result = (result * 255).astype(np.uint8)

        # TODO: turning this into a color image is silly
        print("Result shape", result.shape)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        self.set_output_value("Result", result)

    def draw_config(self):
        super().draw_config()
        self.texture_select.draw()

    def _on_select(self, model):
        print(model)
        with open(model, "rb") as file:
            self.model = pickle.load(file)



class ImageLibraryAttribute(NodeOutput):
    def __init__(self, name, node, library):
        super().__init__(name, node)
        self.library = library
        self.library.on_update(self._on_library_update)
        self.option_dict = {}
        self.preview = None

    def draw(self):
        image_names = self.options()
        with dpg.node_attribute(
            attribute_type=dpg.mvNode_Attr_Output, tag=self.id
        ) as attr:
            self.combo_id = dpg.add_combo(
                image_names, label=self.name, width=200, callback=self._image_selected
            )
            self.preview_container = attr

    def options(self):
        self.option_dict = {}
        for i, img in enumerate(self.library.images):
            key = f"({i}) {img.name}"
            self.option_dict[key] = img
        return [str(k) for k in self.option_dict.keys()]

    def lookup(self, option: str) -> Image:
        return self.option_dict[option]

    def _image_selected(self, caller, app_data):
        image = self.lookup(app_data)
        print(f"Select: {image}")
        if self.preview:
            dpg.delete_item(self.preview)
        self.preview = image.add_to_parent(self.preview_container, width=200)
        self.set_value(image.array)

    def _on_library_update(self):
        image_names = self.options()
        dpg.configure_item(self.combo_id, items=image_names)


class TextureLibraryAttribute(NodeOutput):
    def __init__(self, name, node, library: TextureModelLibrary):
        super().__init__(name, node)
        self.library = library
        self.library.on_update(self._on_library_update)
        self.option_dict = {}
        self.callback = None

    def draw(self):
        image_names = self.options()
        with dpg.node_attribute(
            attribute_type=dpg.mvNode_Attr_Static, tag=self.id
        ) as attr:
            self.combo_id = dpg.add_combo(
                image_names, label=self.name, width=200, callback=self._item_selected
            )
            self.preview_container = attr

            dpg.add_button(label="Create Texture", width=200, height=20, callback=self._on_new_texture_btn)

    def add_callback(self, callback):
        self.callback = callback

    def _on_new_texture_btn(self):
        dpg.show_item("TextureToolWindow")

    def options(self):
        self.option_dict = {}
        for i, path in enumerate(self.library.models):
            key = f"({i}) {Path(path).name}"
            self.option_dict[key] = path
        return [str(k) for k in self.option_dict.keys()]

    def lookup(self, option: str) -> str:
        return self.option_dict[option]

    def _item_selected(self, caller, app_data):
        model = self.lookup(app_data)
        if self.callback:
            self.callback(model)

    def _on_library_update(self):
        image_names = self.options()
        dpg.configure_item(self.combo_id, items=image_names)

class ThresholdNode(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Threshold"
        self.inputs = [
            ImageNodeInput("Image", self),
            NumberSliderAttribute("Threshold", self, 255, 0, 128),
            NumberSliderAttribute("Max", self, 255, 0, 255),
        ]
        self.outputs = [ImageNodeOutput("Result", self)]

    @debounce(0.2)
    def compute(self):
        image = self.get_input_value("Image")
        threshold_value = self.get_input_value("Threshold")
        max_value = self.get_input_value("Max")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(
            gray,
            threshold_value,
            max_value,
            cv2.THRESH_BINARY,
        )
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        self.set_output_value("Result", result)


class CannyNode(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Canny"
        self.inputs = [
            ImageNodeInput("Image", self),
            NumberSliderAttribute("Threshold1", self, 255, 0, 100),
            NumberSliderAttribute("Threshold2", self, 255, 0, 200),
        ]
        self.outputs = [ImageNodeOutput("Result", self)]

    def compute(self):
        image = self.get_input_value("Image")
        t1 = self.get_input_value("Threshold1")
        t2 = self.get_input_value("Threshold2")

        result = cv2.Canny(image, t1, t2)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        self.set_output_value("Result", result)


class TemplateNode(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Template Match"
        self.inputs = [ImageNodeInput("Image", self)]
        self.outputs = [ImageNodeOutput("Result", self)]
        with resources.path('lenscraft.assets', 'CornerTemplate.png') as img_path:
            print("Find template", img_path)
            self.template = cv2.imread(str(img_path))

    def compute(self):
        print("Compute TemplateNode")
        image = self.get_input_value("Image")

        result = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF)
        normalized_result = (result - np.min(result)) / (
            np.max(result) - np.min(result)
        )
        result = (normalized_result * 255).astype(np.uint8)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        self.set_output_value("Result", result)


class MaxPoint(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Min Max"
        self.inputs = [
            ImageNodeInput("Image", self),
            IntNodeInput("OffsetX", self),
            IntNodeInput("OffsetY", self),
        ]
        self.outputs = [
            NodeOutput("MaxPoint", self),
            NodeOutput("MinPoint", self),
            NodeOutput("MaxVal", self),
            NodeOutput("MinVal", self),
        ]

    def compute(self):
        image = self.get_input_value("Image")
        offset_x = self.get_input_value("OffsetX")
        offset_y = self.get_input_value("OffsetY")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)

        max_point = (maxLoc[0] + offset_x, maxLoc[1] + offset_y)
        min_point = (minLoc[0] + offset_x, minLoc[1] + offset_y)

        self.set_output_value("MaxPoint", max_point)
        self.set_output_value("MinPoint", min_point)
        self.set_output_value("MaxVal", maxVal)
        self.set_output_value("MinVal", minVal)


class ShowPoint(Node):
    def __init__(self, context):
        super().__init__()
        self.name = "Show Point"
        self.inputs = [ImageNodeInput("Image", self), NodeInput("Point", self)]
        self.outputs = [ImageNodeOutput("Result", self)]

    def compute(self):
        image = self.get_input_value("Image")
        point = self.get_input_value("Point")

        marked_image = image.copy()
        cv2.circle(marked_image, point, radius=10, color=(255, 0, 0), thickness=-1)
        cv2.imwrite("result.png", marked_image)

        self.set_output_value("Result", marked_image)


class NodeEditor:
    def __init__(self, library: ImageLibrary, texture_library: TextureModelLibrary):
        self.library = library
        self.texture_library = texture_library
        self.id = dpg.generate_uuid()
        self.graph = Graph(library)
        self.graph.add_node(ImageLibraryNode(self))

    def add_to_context(self):
        with dpg.node_editor(
            callback=self.on_link,
            delink_callback=self.on_delink,
            minimap=True,
            minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
            tag=self.id,
        ):
            for node in self.graph.nodes.values():
                node.add_to_editor()

        with dpg.window(
            label="Add Node",
            tag="popup_window",
            no_move=True,
            no_close=True,
            no_resize=True,
            no_collapse=True,
            show=False,
            width=200,
        ):
            options = Node.__subclasses__()
            for option in options:
                dpg.add_button(
                    label=option.__name__,
                    width=-1,
                    callback=self._node_select_callback,
                    user_data=option,
                )

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self._click_callback)
            dpg.add_mouse_release_handler(callback=self._click_up_callback)

    def on_link(self, sender, app_data):
        print(f"link ", app_data)
        a1 = self.graph.get_output(app_data[0])
        a2 = self.graph.get_input(app_data[1])

        new_link = Link(a1, a2)
        print(f"Link {a1.name} to {a2.name}")

        dpg.add_node_link(app_data[0], app_data[1], parent=sender, tag=new_link.id)
        self.graph.add_link(new_link)


    def on_delink(self, sender, app_data):
        print(f"Delink {app_data}")
        self.graph.delink(app_data)
        dpg.delete_item(app_data)

    def _node_select_callback(self, sender, app_data, user_data):
        print("Select Node")
        # user_data is the node class type
        # Create new instance and pass self as context
        new_node = user_data(self)
        new_node.add_to_editor(parent=self.id, pos=self.add_pos)
        self.graph.add_node(new_node)
        dpg.hide_item("popup_window")

    def _click_up_callback(self, sender, app_data):
        if not dpg.is_item_hovered("popup_window"):
            dpg.hide_item("popup_window")

    def _click_callback(self, sender, app_data):
        if app_data == 1:
            self.add_pos = dpg.get_mouse_pos(local=True)
            if dpg.is_item_hovered(self.id):
                dpg.focus_item("popup_window")
                dpg.show_item("popup_window")
                dpg.set_item_pos("popup_window", dpg.get_mouse_pos(local=False))
