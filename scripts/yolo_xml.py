import os
import argparse
import xml.etree.cElementTree as ET

def parse_args():
    parser = argparse.ArgumentParser(description='Convert YOLO annotations to Pascal VOC format.')
    parser.add_argument('--yolo_path', type=str, help='Path to YOLO annotation file')
    parser.add_argument('--image_path', type=str, help='Path to corresponding image file')
    parser.add_argument('--output_path', type=str, help='Path to output Pascal VOC XML file')
    args = parser.parse_args()
    return args

def convert_to_xml(yolo_path, image_path, output_path):
    # Load YOLO annotation file
    with open(yolo_path, 'r') as f:
        annotations = f.readlines()
    
    # Create XML tree
    annotation = ET.Element('annotation')
    
    # Add filename node
    filename = ET.SubElement(annotation, 'filename')
    filename.text = os.path.basename(image_path)
    
    # Add size node
    size = ET.SubElement(annotation, 'size')
    width, height, _ = cv2.imread(image_path).shape
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = '3'
    
    # Add object nodes
    for annotation in annotations:
        class_id, x, y, w, h = annotation.split()
        object_node = ET.SubElement(annotation, 'object')
        ET.SubElement(object_node, 'name').text = 'class' + class_id
        ET.SubElement(object_node, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(int(x) - int(w) // 2)
        ET.SubElement(bndbox, 'ymin').text = str(int(y) - int(h) // 2)
        ET.SubElement(bndbox, 'xmax').text = str(int(x) + int(w) // 2)
        ET.SubElement(bndbox, 'ymax').text = str(int(y) + int(h) // 2)
    
    # Write XML tree to file
    tree = ET.ElementTree(annotation)
    tree.write(output_path)

if __name__ == '__main__':
    args = parse_args()
    convert_to_xml(args.yolo_path, args.image_path, args.output_path)
