import logging
import os
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from PIL import Image
from PIL import ImageDraw

from app.backend.src.exceptions import ImageNotFoundError
from app.backend.src.settings import settings


class Drawer:
    """Класс для отрисовки масок на изображениях какой-то конкретной job"""

    def __init__(self, annotations_xml: Path) -> None:
        self.annotations_xml = annotations_xml

    def get_data(self) -> None:
        """Получить необходимые данные для отрисовки"""

        tree = ET.parse(self.annotations_xml)
        self.__root = tree.getroot()
        labels = self.__root.findall(f"./meta/job/labels//label")
        self.__colors = self.__get_colors(labels)

    def draw_mask(self, image_dict: dict):
        """Рисуем маски"""

        # Получаем image как Element:
        _, image_name = image_dict.popitem()
        condition = lambda x: x.attrib.get("name").split("/")[-1] == image_name
        image = list(filter(condition, self.__root.findall(".//image")))[0]

        # Получаем путь к image:
        image_path = (
            settings.RESULT_PATH
            / str(self.annotations_xml.parent)
            / image_name
        )

        # Создаём объект Image на основе image:
        try:
            image_origin = Image.open(image_path).convert("RGBA")
        except Exception as e:
            ImageNotFoundError(e)

        # Создаём объект маски:
        mask = Image.new(mode="RGBA", size=image_origin.size)
        mask_draw = ImageDraw.Draw(mask)

        # Собираем и сортируем все формы:
        polygons = self.__sort_by_zorder(image.findall(f"./polygon"))
        boxes = self.__sort_by_zorder(image.findall(f"./box"))

        # Отрисовываем маски полигонов
        for polygon in polygons:
            coords = self.__get_coords(polygon, "polygon")
            label = polygon.attrib.get("label")
            try:
                hex_color = self.__colors[label]
            except Exception as e:
                logging.info(
                    f"ERROR: {repr(e)}: not found such color using label: {label}"
                )
                continue
            rgb_color = self.__hex_to_rgb(hex_color)
            rgb_color.append(settings.TRANSPARENCY)
            mask_draw.polygon(coords, fill=tuple(rgb_color))

        # Отрисовываем маски боксов
        for box in boxes:
            coords = self.__get_coords(box, "box")
            label = box.attrib.get("label")
            hex_color = self.__colors[label]
            rgb_color = self.__hex_to_rgb(hex_color)
            rgb_color.append(settings.TRANSPARENCY)
            mask_draw.rectangle(coords, fill=tuple(rgb_color))

        # Наносим маски на изображения:
        if boxes or polygons:
            image_res_file = (
                image_path.parent
                / f"{image_name[0:image_name.rfind('.')]}.png"
            )
            res_image = Image.alpha_composite(image_origin, mask)
            res_image.save(image_res_file)

            # Удаляем старое изображение, если это нужно:
            if image_path != image_res_file:
                os.remove(image_path)

    def remove_xml(self):
        """Удаляем файл annotations.xml"""

        if self.file_xml.exists():
            os.remove(self.file_xml)

    def __get_colors(self, labels: Element) -> dict:
        """Получаем словарь с ключём - lable и значением - код цвета"""

        colors = {}
        for label in labels:
            name = label.find("./name").text
            color = label.find("./color").text
            colors[name] = color
        return colors

    def __sort_by_zorder(
        self, elements: "list[ET.Element]"
    ) -> "list[ET.Element]":
        """Сортируем элементы в порядке наложения (по z_order)"""

        if len(elements) == 0:
            return []
        z_orders = []
        for element in elements:
            z_order = element.attrib.get("z_order")
            z_orders.append(z_order)
        sorted_z_order = sorted(set(z_orders), key=int)
        result: "list[ET.Element]" = []
        for order in sorted_z_order:
            for element in elements:
                if element.attrib.get("z_order") == order:
                    result.append(element)
        return result

    def __get_coords(self, element, type_element):
        """Получаем координаты, исходя из типа элемента"""

        coords = []
        if type_element == "polygon":
            row_coords = element.attrib.get("points").split(";")
            for coord in row_coords:
                x = float(coord.split(",")[0])
                y = float(coord.split(",")[1])
                coords.append((x, y))
        elif type_element == "box":
            xtl = float(element.attrib.get("xtl"))
            ytl = float(element.attrib.get("ytl"))
            xbr = float(element.attrib.get("xbr"))
            ybr = float(element.attrib.get("ybr"))
            coords.extend([xtl, ytl, xbr, ybr])
        return coords

    def __hex_to_rgb(self, hex_color):
        only_numbers = hex_color.lstrip("#")
        rgb_color_code = [int(only_numbers[i : i + 2], 16) for i in (0, 2, 4)]
        return rgb_color_code
