import math
import arrow

def convert_array_file_size(items):
   for item in items:
      item['size'] = convert_size(item['size'])
      item['regDate'] = arrow.get(item['regDate']).to('Africa/Kigali').humanize()
   return items


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])