import numpy as np

a = np.arange(15)
pixels = [
   (54, 54, 54), (232, 23, 93), (71, 71, 71), (168, 167, 167),
   (204, 82, 122), (54, 54, 54), (168, 167, 167), (232, 23, 93),
   (71, 71, 71), (168, 167, 167), (54, 54, 54), (204, 82, 122),
   (168, 167, 167), (204, 82, 122), (232, 23, 93), (54, 54, 54)
]

# # Convert the pixels into an array using numpy
# array = np.array(pixels, dtype=np.uint8)


array = np.array_split(pixels, 2)

array = np.array(array, dtype=np.uint8)
print(array)
