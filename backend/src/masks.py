import os

from PIL import Image
from PIL import ImageDraw

from backend.src.settings import settings
from backend.src.utils import _get_coords
from backend.src.utils import hex_to_rgb
from backend.src.utils import sort_by_zorder


def drow_masks(images, colors, _id, transparency, type_element):
    """
    Create masks and drow it into the images
    """
    for image in images:
        image_id = image.attrib.get("id")
        image_path = settings.RESULT_PATH / str(_id) / f"{image_id}.jpeg"

        image_origin = Image.open(image_path).convert("RGBA")
        mask = Image.new(mode="RGBA", size=image_origin.size)
        draw = ImageDraw.Draw(mask)

        elements = image.findall(f"./{type_element}")
        elements = sort_by_zorder(elements)
        for element in elements:
            coords = _get_coords(element, type_element)
            label = element.attrib.get("label")
            hex_color = colors[label]
            rgb_color = hex_to_rgb(hex_color)
            rgb_color.append(transparency)
            if type_element == "polygon":
                draw.polygon(coords, fill=tuple(rgb_color))
            elif type_element == "box":
                draw.rectangle(coords, fill=tuple(rgb_color))

        image_res_file = image_path.parent / f"{image_id}.png"
        res_image = Image.alpha_composite(image_origin, mask)
        res_image.save(image_res_file)
        if image_path.exists():
            try:
                os.remove(image_path)
            except:
                print(f"deleting was failed: {image_id}")
