import xml.etree.ElementTree as ET
from PIL import Image
import os
import xml.dom.minidom

def get_image_size(image_path):
    img = Image.open(image_path)
    return img.size


def get_image_depth(image_path):
    img = Image.open(image_path)
    return len(img.mode.split())


def read_file(file_path):
    with open(file_path, "r", encoding='ISO-8859-1') as f:
        lines = f.readlines()
    return lines


def calc_xmin(v1, v3, width):
    xmin = int((float(v1) - float(v3) / 2) * width)
    return xmin


def calc_ymin(v2, v4, height):
    ymin = int((float(v2) - float(v4) / 2) * height)
    return ymin


def calc_xmax(v1, v3, width):
    xmax = int((float(v1) + float(v3) / 2) * width)
    return xmax


def calc_ymax(v2, v4, height):
    ymax = int((float(v2) + float(v4) / 2) * height)
    return ymax


def store_objects(lines, image_path):
    objects = []
    width, height = get_image_size(image_path)
    for line in lines:
        parts = line.strip().split(" ")
        if parts[0] == "0":
            obj_class = "fall"
        elif parts[0] == "1":
            obj_class = "stand"
        elif parts[0] == "2":
            obj_class = "sit"
        else:
            obj_class = "unknown"
        obj = {
            "class": obj_class,        
            "xmin": calc_xmin(parts[1], parts[3], width),
            "ymin": calc_ymin(parts[2], parts[4], height),
            "xmax": calc_xmax(parts[1], parts[3], width),
            "ymax": calc_ymax(parts[2], parts[4], height),
        }
        objects.append(obj)
    return objects


def format_xml(file_path):
    with open(file_path, "r", encoding='ISO-8859-1') as f:
        xml_data = f.read()

    dom = xml.dom.minidom.parseString(xml_data)
    xml_formatted = dom.toprettyxml(indent="\t")

    with open(file_path, "w", encoding='ISO-8859-1') as f:
        f.write(xml_formatted)


def write_pascal_voc_xml(image_path, objects, xml_path):
    image_name = os.path.basename(image_path)
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = os.path.dirname(image_path)
    ET.SubElement(root, "filename").text = image_name
    ET.SubElement(root, "path").text = image_path
    size = ET.SubElement(root, "size")
    width, height = get_image_size(image_path)
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(get_image_depth(image_path))
    ET.SubElement(root, "segmented").text = "0"
    for obj in objects:
        obj_elem = ET.SubElement(root, "object")
        ET.SubElement(obj_elem, "name").text = obj["class"]
        ET.SubElement(obj_elem, "pose").text = "Unspecified"
        ET.SubElement(obj_elem, "truncated").text = "0"
        ET.SubElement(obj_elem, "difficult").text = "0"
        bbox = ET.SubElement(obj_elem, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(obj["xmin"])
        ET.SubElement(bbox, "ymin").text = str(obj["ymin"])
        ET.SubElement(bbox, "xmax").text = str(obj["xmax"])
        ET.SubElement(bbox, "ymax").text = str(obj["ymax"])
    tree = ET.ElementTree(root)
    tree.write(xml_path)
    format_xml(xml_path)


def txt_pascal_voc_main(path):
    for file in os.listdir(path):
        if file.endswith(".txt"):
            file_path = os.path.join(path, file)
            lines = read_file(file_path)

            jpgfile = os.path.join(path, os.path.splitext(file)[0] + ".jpg")
            xmlfile = os.path.join(path, os.path.splitext(file)[0] + ".xml")
            
            objects = store_objects(lines, jpgfile)

            write_pascal_voc_xml(jpgfile, objects, xmlfile)
            

if __name__ == "__main__":
    # PATH CONFIGURATION
    path1 = "images/test"
    path2 = "images/train"

    txt_pascal_voc_main(path1)
    txt_pascal_voc_main(path2)
