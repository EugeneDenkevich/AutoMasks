import os
import pathlib as pt
import random
import shutil
import xml.dom.minidom

from PIL import Image
from PIL import ImageDraw


class Drawer:
    root_dir = pt.Path(__file__).parent.resolve()
    results_dir = root_dir / "results"
    images_dir = root_dir / "images"
    tmp_dir = root_dir / "tmp"
    without_markup = root_dir / "without_markup"

    photo_mask_path = "images/"
    color_by_name = {}
    colors = []
    file_to_parse = "annotations4.xml"

    def labels_colors(self):
        doc = xml.dom.minidom.parse(self.file_to_parse)
        labels = doc.getElementsByTagName("label")
        for label in labels:
            name_el = label.getElementsByTagName("name")[0]
            color_el = label.getElementsByTagName("color")[0]

            hex_value = color_el.firstChild.nodeValue.strip("#")

            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)

            color_RGB = (r, g, b)
            self.color_by_name[name_el.firstChild.nodeValue] = color_RGB

    @staticmethod
    def __generate_random_color() -> str:
        symbols = "ABCDEF0123456789"
        color = "#"
        for _ in range(6):
            color += random.choice(symbols)

        return color

    def __get_color(self) -> str:
        while True:
            color = self.__generate_random_color()
            if color not in self.colors:
                self.colors.append(color)
                return color

    def parse(self):
        if not self.results_dir.exists():
            os.makedirs(self.results_dir)
        if not self.tmp_dir.exists():
            os.makedirs(self.tmp_dir)
        if not self.without_markup.exists():
            os.makedirs(self.without_markup)

        doc = xml.dom.minidom.parse(self.file_to_parse)
        image_quantity = 0  # счетчик обработанных изображений
        images = doc.getElementsByTagName("image")
        colors = {}
        for image in images:
            index_file = image.getAttribute("name").rfind("/")
            image_name = image.getAttribute("name")[
                index_file + 1 :
            ]  # имя файла
            short_image_name = image_name[: image_name.rfind(".")]
            print(image_name)

            width = image.getAttribute("width")
            height = image.getAttribute("height")  # разрешение изображения

            a = []
            try:
                image_i = Image.open(
                    self.images_dir / image_name
                )  # открываем фото
            except Exception as e:
                print(f"Ошибка: {e} Изображение: {image_name}")

            wall_segmentation = Image.new(
                "RGBA", (int(width), int(height)), (0, 0, 0)
            )
            wall_instances = Image.new(
                "RGBA", (int(width), int(height)), (0, 0, 0)
            )
            floor_segmentation = Image.new(
                "RGBA", (int(width), int(height)), (0, 0, 0)
            )
            floor_instances = Image.new(
                "RGBA", (int(width), int(height)), (0, 0, 0)
            )

            overlay = Image.new(
                "RGBA", (int(width), int(height)), (0, 0, 0, 0)
            )
            draw = ImageDraw.Draw(overlay)

            # overlay is used to display results on 1 images, not needed in the final version of output
            draw_ws = ImageDraw.Draw(wall_segmentation)
            draw_fs = ImageDraw.Draw(floor_segmentation)
            draw_wi = ImageDraw.Draw(wall_instances)
            draw_fi = ImageDraw.Draw(floor_instances)
            polygons = image.getElementsByTagName("polygon")
            for polygon in polygons:
                label = polygon.getAttribute("label")

                group_id = polygon.getAttribute("group_id")
                if group_id in colors:
                    color = colors[group_id]
                elif not group_id:
                    color = self.__get_color()
                else:
                    color = self.__get_color()
                    colors[group_id] = color
                a.append(label)
                polygon_data = polygon.getAttribute("points").replace(";", ",")
                points = tuple(
                    map(float, polygon_data.split(","))
                )  # формируем кортеж координат
                if label == "background":  # игнорируем класс Ignoreё
                    continue
                elif label == "column" or label == "wall":
                    draw_ws.polygon(
                        points, outline=(255, 255, 255), fill=(255, 255, 255)
                    )
                    draw_wi.polygon(points, outline=color, fill=color)
                    hex_value = color.strip("#")
                    r = int(hex_value[0:2], 16)
                    g = int(hex_value[2:4], 16)
                    b = int(hex_value[4:6], 16)
                    color = (r, g, b)
                    color_new = (color[0], color[1], color[2], 200)
                    draw.polygon(points, outline=color_new, fill=color_new)
                elif label == "floor":
                    draw_fs.polygon(
                        points, outline=(255, 255, 255), fill=(255, 255, 255)
                    )
                    draw_fi.polygon(points, outline=color, fill=color)
                    hex_value = color.strip("#")
                    r = int(hex_value[0:2], 16)
                    g = int(hex_value[2:4], 16)
                    b = int(hex_value[4:6], 16)
                    color = (r, g, b)
                    color_new = (color[0], color[1], color[2], 200)
                    draw.polygon(points, outline=color_new, fill=color_new)

            boxs = image.getElementsByTagName("box")
            for box in boxs:
                label = box.getAttribute("label")
                group_id = box.getAttribute("group_id")
                if group_id in colors:
                    color = colors[group_id]
                elif not group_id:
                    color = self.__get_color()

                else:
                    color = self.__get_color()
                    colors[group_id] = color
                x1 = box.getAttribute("xtl")
                y1 = box.getAttribute("ytl")
                x2 = box.getAttribute("xbr")
                y2 = box.getAttribute("ybr")
                a.append(label)
                if label == "background":  # игнорируем класс Ignor
                    continue
                elif label == "column" or label == "wall":
                    draw_ws.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(255, 255, 255),
                        fill=(255, 255, 255),
                    )
                    draw_wi.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=color,
                        fill=color,
                    )
                    hex_value = color.strip("#")
                    r = int(hex_value[0:2], 16)
                    g = int(hex_value[2:4], 16)
                    b = int(hex_value[4:6], 16)
                    color = (r, g, b)
                    color_new = (color[0], color[1], color[2], 200)
                    draw.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=color_new,
                        fill=color_new,
                    )
                elif label == "floor":
                    draw_fs.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(255, 255, 255),
                        fill=(255, 255, 255),
                    )
                    draw_fi.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=color,
                        fill=color,
                    )
                    hex_value = color.strip("#")
                    r = int(hex_value[0:2], 16)
                    g = int(hex_value[2:4], 16)
                    b = int(hex_value[4:6], 16)
                    color = (r, g, b)
                    color_new = (color[0], color[1], color[2], 200)
                    draw.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=color_new,
                        fill=color_new,
                    )

            for polygon in polygons:
                label = polygon.getAttribute("label")
                if label == "background":
                    polygon_data = polygon.getAttribute("points").replace(
                        ";", ","
                    )
                    points = tuple(
                        map(float, polygon_data.split(","))
                    )  # формируем кортеж координат
                    draw_wi.polygon(points, outline=(0, 0, 0), fill=(0, 0, 0))
                    draw_ws.polygon(points, outline=(0, 0, 0), fill=(0, 0, 0))
                    draw_fs.polygon(points, outline=(0, 0, 0), fill=(0, 0, 0))
                    draw_fi.polygon(points, outline=(0, 0, 0), fill=(0, 0, 0))
                    draw.polygon(
                        points, outline=(0, 0, 0, 0), fill=(0, 0, 0, 0)
                    )

            boxs = image.getElementsByTagName("box")
            for box in boxs:
                label = box.getAttribute("label")
                if label == "background":
                    x1 = box.getAttribute("xtl")
                    y1 = box.getAttribute("ytl")
                    x2 = box.getAttribute("xbr")
                    y2 = box.getAttribute("ybr")
                    draw_ws.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(0, 0, 0),
                        fill=(0, 0, 0),
                    )
                    draw_wi.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(0, 0, 0),
                        fill=(0, 0, 0),
                    )
                    draw_fs.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(0, 0, 0),
                        fill=(0, 0, 0),
                    )
                    draw_fi.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(0, 0, 0),
                        fill=(0, 0, 0),
                    )
                    draw.rectangle(
                        ((float(x1), float(y1)), (float(x2), float(y2))),
                        outline=(0, 0, 0, 0),
                        fill=(0, 0, 0, 0),
                    )

            if len(a) != 0:
                wall_segmentation.save(f"results/{short_image_name}_ws.png")
                wall_instances.save(f"results/{short_image_name}_wi.png")
                floor_segmentation.save(f"results/{short_image_name}_fs.png")
                floor_instances.save(f"results/{short_image_name}_fi.png")
                result = Image.alpha_composite(
                    image_i.convert("RGBA"), overlay
                )
                result.save(f"tmp/{short_image_name}_tmp.png")
                image_quantity += 1
                print(image_quantity)
            else:
                try:
                    current_path = str(
                        (
                            pt.Path(__file__).parent / "images" / image_name
                        ).resolve()
                    )
                    target_path = str(
                        (
                            pt.Path(__file__).parent
                            / "without_markup"
                            / image_name
                        ).resolve()
                    )
                    shutil.copyfile(current_path, target_path)
                    print(f"Файл {image_name} скопирован в {target_path}")
                except Exception as e:
                    print(
                        f"Ошибка: {e} Изображение: {self.photo_mask_path}{image_name}"
                    )

        print(f"Готово! Всего обработано изображений: {image_quantity}")


drawer = Drawer()
# drawer.labels_colors()
# drawer.parse()
