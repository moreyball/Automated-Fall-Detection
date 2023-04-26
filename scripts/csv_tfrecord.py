import tensorflow as tf
import csv

# Define a function to parse each row of the CSV file and convert it to a TFExample object.
def parse_csv_row(row):
    filename, width, height, obj_class, xmin, ymin, xmax, ymax = row
    xmin = int(xmin)
    ymin = int(ymin)
    xmax = int(xmax)
    ymax = int(ymax)

    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                "filename": tf.train.Feature(
                    bytes_list=tf.train.BytesList(value=[filename.encode("utf-8")])
                ),
                "width": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[int(width)])
                ),
                "height": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[int(height)])
                ),
                "class": tf.train.Feature(
                    bytes_list=tf.train.BytesList(value=[obj_class.encode("utf-8")])
                ),
                "xmin": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[int(xmin)])
                ),
                "ymin": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[int(ymin)])
                ),
                "xmax": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[int(xmax)])
                ),
                "ymax": tf.train.Feature(
                    int64_list=tf.train.Int64List(value=[int(ymax)])
                ),
            }
        )
    )

    return example


def train_tfrecord():
    # Parse the CSV file and convert each row to a TFExample object.
    csv_file = "annotations/train.csv"
    output_file = "annotations/train.tfrecord"
    with tf.io.TFRecordWriter(output_file) as writer:
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            for row in reader:
                example = parse_csv_row(row)
                writer.write(example.SerializeToString())


def test_tfrecord():
    # Parse the CSV file and convert each row to a TFExample object.
    csv_file = "annotations/test.csv"
    output_file = "annotations/test.tfrecord"
    with tf.io.TFRecordWriter(output_file) as writer:
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            for row in reader:
                example = parse_csv_row(row)
                writer.write(example.SerializeToString())


if __name__ == "__main__":
    train_tfrecord()
    test_tfrecord()
