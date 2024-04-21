import napari
import numpy as np

from image_io import ImageIO
from parametrization import Sphere
from scipy.spatial import ConvexHull

from time import time


image = ImageIO()
image.readMRC(
    "/Users/vmaurer/Documents/PhD/Projects/influenza_reconstruction.nosync/raw.nosync/TS_01oa_rec_bin4.mrc",
    memmap=False,
)
viewer = napari.view_image(image.data, name="photographer")

sphere = Sphere(center=(100, 100, 100), radius=100)
points = sphere.sample(200)
print(points.shape)

start = time()
hull = ConvexHull(points)
print(hull.simplices.shape)

surface = (hull.points, hull.simplices, 1000 * np.ones(hull.points.shape[0]))
viewer.add_surface(
    surface,
    name="hull",
    colormap="red",
    opacity=1,
    blending="translucent",
    shading="none",
    visible=True,
)

print(time() - start)


# viewer.add_points(
#     points,
#     name="Points",
#     edge_width=0,
#     size=3,
#     symbol="ring",
# )


napari.run()
