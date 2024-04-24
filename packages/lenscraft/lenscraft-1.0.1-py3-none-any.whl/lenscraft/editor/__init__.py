import dearpygui.dearpygui as dpg
import json

from lenscraft.image import ImageLibrary
from lenscraft.nodes import NodeEditor
from lenscraft.texture import TextureModelLibrary
from lenscraft.texture.tool import TextureClassifierTool

def print_me(sender):
    print(f"Menu Item: {sender}")


class EditorWindow:
    def __init__(self, image_library: ImageLibrary, texture_library: TextureModelLibrary):
        self.image_library = image_library
        self.texture_library = texture_library
        self.texture_tool = TextureClassifierTool(image_library, texture_library)

    def load_project_callback(self, caller, app_data):
        print(f"Load project {app_data}")
        project_file_path = app_data["file_path_name"]
        self.load_project(file_path=project_file_path)

    def load_project(self, file_path="project.json"):
        print(f"Load project {file_path}")
        try:
            with open(file_path, "r") as file:
                project = json.load(file)
                print(project)
                for path in project["images"]:
                    self.image_library.load(path)

            self.update_images()

        except FileNotFoundError:
            print(f"No saved image selection found at '{file_path}'")


    def save_project_callback(self, caller, app_data):
        print(f"Save project {app_data}")
        project_file_path = app_data["file_path_name"]
        self.save_project(project_file_path)

    def save_project(self, project_file_path):
        try:
            with open(project_file_path, "w") as file:
                image_paths = [img.path for img in self.image_library.images]
                json.dump({"images": image_paths}, file)

        except Exception as ex:
            print(ex)


    def load_images(self, sender, app_data):
        for name, path in app_data["selections"].items():
            print(f"Load image {path}")  # Use print for demonstration
            self.image_library.load(path)

        self.update_images()


    def update_images(self):
        dpg.delete_item("image_row", children_only=True)  # Clear existing images

        with dpg.group(parent="image_row", horizontal=True):
            for image in self.image_library.images:
                image.show_in_context()


    def add_to_context(self):
        # Create a window that fills the viewport and cannot be moved or closed
        with dpg.window(
            tag="primary",
            no_move=True,
            no_close=True,
            no_title_bar=True,
            menubar=True,
        ):
            image_row = dpg.add_child_window(
                width=-1,
                height=200,
                autosize_x=True,
                horizontal_scrollbar=True,
                tag="image_row",
            )

            with dpg.file_dialog(
                directory_selector=False,
                show=False,
                callback=self.load_images,
                id="file_dialog_id",
                width=700,
                height=400,
            ):
                dpg.add_file_extension(".*")
                dpg.add_file_extension("", color=(150, 255, 150, 255))
                dpg.add_file_extension(
                    ".jpg, .png", color=(0, 255, 255, 255)
                )  # More specific filter

            with dpg.file_dialog(
                directory_selector=False,
                default_filename="project",
                show=False,
                callback=self.save_project_callback,
                id="save_project_dialog",
                width=700,
                height=400,
            ):
                dpg.add_file_extension(".json", color=(0, 255, 255, 255))

            with dpg.file_dialog(
                directory_selector=False,
                default_filename="project",
                show=False,
                callback=self.load_project_callback,
                id="load_project_dialog",
                width=700,
                height=400,
            ):
                dpg.add_file_extension(".json", color=(0, 255, 255, 255))

            editor = NodeEditor(self.image_library, self.texture_library)
            with dpg.child_window(label="Node Editor", width=-1):
                editor.add_to_context()

            self.texture_tool.add_to_context()

def run_gui():
    image_library = ImageLibrary()
    texture_library = TextureModelLibrary()
    editor = EditorWindow(image_library, texture_library)

    dpg.create_context()

    # Create a viewport
    viewport_width = 1024
    viewport_height = 800
    dpg.create_viewport(
        title="Lens Craft", width=viewport_width, height=viewport_height
    )

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(
                label="Add Images", callback=lambda: dpg.show_item("file_dialog_id")
            )
            dpg.add_menu_item(
                label="Load Project", callback=lambda: dpg.show_item("load_project_dialog")
            )
            dpg.add_menu_item(
                label="Save Project", callback=lambda: dpg.show_item("save_project_dialog")
            )

        dpg.add_menu_item(label="Help", callback=print_me)

    editor.add_to_context()


    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary", True)

    dpg.start_dearpygui()

    dpg.destroy_context()