import os

from PIL import Image
from PIL import ImageDraw
from src.settings import settings
from src.utils import _get_coords
from src.utils import hex_to_rgb
from src.utils import sort_by_zorder


def drow_masks(images, colors, _id, transparency):
    """
    Create masks and drow it into the images
    """
    for image in images:
        image_id = image.attrib.get("id")
        image_path = settings.RESULT_PATH / str(_id) / f"{image_id}.jpeg"

        image_origin = Image.open(image_path).convert("RGBA")
        mask = Image.new(mode="RGBA", size=image_origin.size)
        draw = ImageDraw.Draw(mask)

        polygons = image.findall("./polygon")
        polygons = sort_by_zorder(polygons)
        for polygon in polygons:
            coords = _get_coords(polygon)
            label = polygon.attrib.get("label")
            hex_color = colors[label]
            rgb_color = hex_to_rgb(hex_color)
            rgb_color.append(transparency)
            draw.polygon(coords, fill=tuple(rgb_color))

        image_res_file = image_path.parent / f"{image_id}.png"
        res_image = Image.alpha_composite(image_origin, mask)
        res_image.save(image_res_file)
        if image_path.exists():
            try:
                os.remove(image_path)
            except:
                print(f"deleting was failed: {image_id}")
