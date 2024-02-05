import os
from xml.etree.ElementTree import Element

from PIL import Image
from PIL import ImageDraw

from backend.src.settings import settings
from backend.src.utils import _get_coords
from backend.src.utils import hex_to_rgb
from backend.src.utils import sort_by_zorder
from utils.main_process import main_process
from utils.main_process import process_end


def drow_masks(images: list[Element], colors, _id, transparency):
    """
    Create masks and drow it into the images
    """
    for image in images:
        will_draw = 0
        if not main_process.over:
            image_name = image.attrib.get("name").split("/")[-1]
            image_path = settings.RESULT_PATH / str(_id) / image_name

            try:
                image_origin = Image.open(image_path).convert("RGBA")
            except Exception as e:
                print(f"WARNING: {e}: {image_name}")
                continue
            mask = Image.new(mode="RGBA", size=image_origin.size)
            mask_draw = ImageDraw.Draw(mask)

            polygons = sort_by_zorder(image.findall(f"./polygon"))
            boxes = sort_by_zorder(image.findall(f"./box"))

        else:
            process_end()
            return

        for polygon in polygons:
            will_draw += 1
            if not main_process.over:
                coords = _get_coords(polygon, "polygon")
                label = polygon.attrib.get("label")
                try:
                    hex_color = colors[label]
                except Exception as e:
                    print(
                        f"ERROR: {repr(e)}: not found such color using label: {label}"
                    )
                    continue
                rgb_color = hex_to_rgb(hex_color)
                rgb_color.append(transparency)
                mask_draw.polygon(coords, fill=tuple(rgb_color))
            else:
                process_end()
                return

        for box in boxes:
            will_draw += 1
            if not main_process.over:
                coords = _get_coords(box, "box")
                label = box.attrib.get("label")
                hex_color = colors[label]
                rgb_color = hex_to_rgb(hex_color)
                rgb_color.append(transparency)
                mask_draw.rectangle(coords, fill=tuple(rgb_color))
            else:
                process_end()
                return

        if will_draw:
            image_res_file = (
                image_path.parent / f"{image_name.split('.')[0]}.png"
            )
            res_image = Image.alpha_composite(image_origin, mask)
            res_image.save(image_res_file)


"""
Почему папка не открывается?
И Пройтись по методам THX.
"""
