import os
import csv
import xml.etree.ElementTree as ET


def w_header(writer):
    header = [
        "filename",
        "width",
        "height",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    writer.writerow(header)


def w_data(writer, xml_path):
    for file in os.listdir(xml_path):
        xmlfile = os.path.join(xml_path, file)
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        for member in root.findall("object"):
            value = (
                str(file),
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                int(member[1][0].text),
                int(member[1][1].text),
                int(member[1][2].text),
                int(member[1][3].text),
            )
            writer.writerow(value)


def open_csv(xml_path1, xml_path2):
    with open("annotations/train.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        w_header(writer)
        w_data(writer, xml_path1)
        w_data(writer, xml_path2)


if __name__ == "__main__":
    # PATH CONFIGURATION
    xml_path1 = "xml/train"
    xml_path2 = "xml/val"

    open_csv(xml_path1, xml_path2)