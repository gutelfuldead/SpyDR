# create_stego_zip_jpg.py - Hide a zip file inside a JPEG

import sys

# Start with a jpeg file
jpg_file = open(sys.argv[1], 'rb')  # Path to JPEG
jpg_data = jpg_file.read()
jpg_file.close()

# And the zip file to embed in the jpeg
zip_file = open(sys.argv[2], 'rb')  # Path to ZIP file
zip_data = zip_file.read()
zip_file.close()

# Combine the files
out_file = open('special_image.jpg', 'wb')  # Output file
out_file.write(jpg_data)
out_file.write(zip_data)
out_file.close()

# The resulting output file appears like a normal jpeg but can also be
# unzipped and used as an archive.
