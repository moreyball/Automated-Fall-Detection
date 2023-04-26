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
    with open(file_path, "r") as f:
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
        obj = {
            "class": parts[0],
            "xmin": calc_xmin(parts[1], parts[3], width),
            "ymin": calc_ymin(parts[2], parts[4], height),
            "xmax": calc_xmax(parts[1], parts[3], width),
            "ymax": calc_ymax(parts[2], parts[4], height),
        }
        objects.append(obj)
    return objects


def format_xml(file_path):
    with open(file_path, "r") as f:
        xml_data = f.read()

    dom = xml.dom.minidom.parseString(xml_data)
    xml_formatted = dom.toprettyxml(indent="\t")

    with open(file_path, "w") as f:
        f.write(xml_formatted)


def write_xml(width, height, depth, objects, xml_path):
    root = ET.Element("annotation")
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    for obj in objects:
        object_elem = ET.SubElement(root, "object")
        ET.SubElement(object_elem, "name").text = obj["class"]

        bbox = ET.SubElement(object_elem, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(obj["xmin"])
        ET.SubElement(bbox, "ymin").text = str(obj["ymin"])
        ET.SubElement(bbox, "xmax").text = str(obj["xmax"])
        ET.SubElement(bbox, "ymax").text = str(obj["ymax"])

    tree = ET.ElementTree(root)
    tree.write(xml_path)


if __name__ == "__main__":
    # PATH CONFIGURATION
    text_path1 = "fall_dataset/labels/train"
    jpg_path1 = "fall_dataset/images/train"
    xml_path1 = "xml/train"
    
    text_path2 = "fall_dataset/labels/val"
    jpg_path2 = "fall_dataset/images/val"
    xml_path2 = "xml/val"

    for file in os.listdir(text_path1):
        file_path = os.path.join(text_path1, file)
        lines = read_file(file_path)

        txtfile = os.path.join(text_path1, file)
        jpgfile = os.path.join(jpg_path1, os.path.splitext(file)[0] + ".jpg")
        xmlfile = os.path.join(xml_path1, os.path.splitext(file)[0] + ".xml")

        objects = store_objects(lines, jpgfile)
        width, height = get_image_size(jpgfile)
        depth = get_image_depth(jpgfile)
        write_xml(width, height, depth, objects, xmlfile)
        format_xml(xmlfile)
        
    for file in os.listdir(text_path2):
        file_path = os.path.join(text_path2, file)
        lines = read_file(file_path)

        txtfile = os.path.join(text_path2, file)
        jpgfile = os.path.join(jpg_path2, os.path.splitext(file)[0] + ".jpg")
        xmlfile = os.path.join(xml_path2, os.path.splitext(file)[0] + ".xml")
        if(os.path.exists(jpgfile)):
            pass
        else:
            jpgfile = os.path.join(jpg_path2, os.path.splitext(file)[0] + ".png")
        objects = store_objects(lines, jpgfile)
        width, height = get_image_size(jpgfile)
        depth = get_image_depth(jpgfile)
        write_xml(width, height, depth, objects, xmlfile)
        format_xml(xmlfile)
