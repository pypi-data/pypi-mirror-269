import logging
import threading
from typing import List
import dearpygui.dearpygui as dpg
import cv2
import numpy as np
import pathlib


def ArrToData(texture):
    auxImg = cv2.cvtColor(texture, cv2.COLOR_BGR2BGRA)
    auxImg = np.asfarray(auxImg, dtype="f")
    auxImg = auxImg.ravel()
    auxImg = np.true_divide(auxImg, 255.0)
    return auxImg


class Image:
    def __init__(self, id, path, array):
        self.texture_id = id
        self.path = path
        self.array = array

    @property
    def width(self):
        return self.array.shape[1]

    @property
    def height(self):
        return self.array.shape[0]

    @property
    def name(self) -> str:
        return pathlib.Path(self.path).name

    def show_in_context(self, img_height=180):
        """Call in a dpg context to add this image"""
        img_width = (self.width / self.height) * img_height
        dpg.add_image(self.texture_id, width=img_width, height=img_height)

    def add_to_parent(self, parent, width=None, height=None):
        (img_width,img_height) = self.fit(width, height)

        return dpg.add_image(
            self.texture_id, width=img_width, height=img_height, parent=parent
        )
    
    def add_to_context(self, width=None, height=None):
        """Same as add to parent, but the parent is inferred from the dpg container stack"""
        (img_width,img_height) = self.fit(width, height)

        return dpg.add_image(self.texture_id, width=img_width, height=img_height)
    
    def draw_image(self, width=None, height=None):
        (img_width,img_height) = self.fit(width, height)

        return dpg.draw_image(self.texture_id, (0,0), (img_width,img_height))

    def fit(self, width=None, height=None):
        """Return image dimensions that fit the constraint based on aspect ratio"""
        if width:
            img_width = width
            img_height = (self.height / self.width) * width
        elif height:
            img_height = height
            img_width = (self.width / self.height) * height
        else:
            raise Exception("Provide either width or height")
        
        return (img_width, img_height)

    def update_pixels(self, new_array):
        dpg.set_value(self.texture_id, ArrToData(new_array))

    @staticmethod
    def load(path):
        print(f"Load image {path}")
        width, height, channels, data = dpg.load_image(path)
        image_array = cv2.imread(path)
        texture_id = dpg.generate_uuid()
        with dpg.texture_registry(show=False):
            dpg.add_dynamic_texture(width, height, default_value=data, tag=texture_id)

        return Image(texture_id, path, image_array)

    def __repr__(self) -> str:
        return f"Image({self.path})"


class DynamicTexture:
    delete_texture_queue = []

    def __init__(self, arr):
        self._texture_id = None
        self._new_texture_data(arr)

    @property
    def height(self):
        return dpg.get_item_configuration(self._texture_id)["height"]

    @property
    def width(self):
        return dpg.get_item_configuration(self._texture_id)["width"]

    def update(self, arr):
        if arr.shape[0] != self.height or arr.shape[1] != self.width:
            self._new_texture_data(arr)
        else:
            dpg.set_value(self._texture_id, ArrToData(arr))

    def add_to_parent(self, parent, width=None, height=None):
        if width:
            img_width = width
            img_height = (self.height / self.width) * width
        elif height:
            img_height = height
            img_width = (self.width / self.height) * height
        else:
            raise Exception("Provide either width or height")

        return dpg.add_image(
            self._texture_id, width=img_width, height=img_height, parent=parent
        )

    def _new_texture_data(self, arr):
        old_texture_id = self._texture_id
        self._texture_id = dpg.generate_uuid()
        data = ArrToData(arr)
        with dpg.texture_registry(show=False):
            height, width = arr.shape[0], arr.shape[1]
            dpg.add_dynamic_texture(
                width, height, default_value=data, tag=self._texture_id
            )
            if old_texture_id is not None:
                # We need to delete the old texture to avoid memory leak
                # Cant delete it immediately because that causes a race condition that can lead to a segfault
                # Run cleanup after few milliseconds
                DynamicTexture.delete_texture_queue.append(old_texture_id)
                threading.Timer(0.5, DynamicTexture.delete_old).start()

    @staticmethod
    def delete_old():
        while len(DynamicTexture.delete_texture_queue) > 0:
            tid = DynamicTexture.delete_texture_queue.pop()
            dpg.delete_item(tid)


class ImageLibrary:
    def __init__(self):
        self.images: List[Image] = []
        self._on_update_callbacks = []

    def add_image(self, image):
        self.images.append(image)
        self._trigger_on_update()

    def on_update(self, callback):
        """Register callback that will be called if the list of images changes"""
        self._on_update_callbacks.append(callback)

    def load(self, path):
        width, height, channels, data = dpg.load_image(path)
        image_array = cv2.imread(path)
        texture_id = dpg.generate_uuid()
        with dpg.texture_registry(show=False):
            dpg.add_dynamic_texture(width, height, default_value=data, tag=texture_id)

        new_image = Image(texture_id, path, image_array)
        self.add_image(new_image)

    def _trigger_on_update(self):
        for callback in self._on_update_callbacks:
            try:
                callback()
            except Exception as ex:
                logging.warning(ex)
