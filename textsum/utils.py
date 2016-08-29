from __future__ import print_function

import glob
import random
import struct
import argparse

from tensorflow.core.example import example_pb2


def decodeData(recordio_path):
  """decodes the data, shipped with textsum model, from recordio format to text
  format
  Args:
    recordio_path: CNS path to tf.Example recordio
  Yields:
    Deserialized tf.Example.
  If there are multiple files specified, they accessed in a random order.
  """
  filelist = glob.glob(recordio_path)
  assert filelist, 'Empty filelist.'
  random.shuffle(filelist)
  for f in filelist:
    reader = open(f, 'rb')
    while True:
      len_bytes = reader.read(8)
      if not len_bytes: break
      str_len = struct.unpack('q', len_bytes)[0]
      example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
      yield example_pb2.Example.FromString(example_str)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--recordio_path', type=str, default='data/data',
                        help='Path to data in recordio format')
  args = parser.parse_args()
  for i in decodeData(args.recordio_path):
    print(i)
