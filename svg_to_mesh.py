import svgpathtools  as spt
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

paths, attributes, svg_attributes = spt.svg2paths2('/Users/tahlia/Downloads/frontback.svg')

def svgpathtools_unpacker(obj, sample_points=10):
    path = []
    if isinstance(obj, (spt.path.Path, list)):
        for i in obj:
            path.extend(svgpathtools_unpacker(i, sample_points=sample_points))
    elif isinstance(obj, spt.path.Line):
        path.extend(obj.bpoints())
    elif isinstance(obj, (spt.path.CubicBezier, spt.path.QuadraticBezier)):
        path.extend(obj.points(np.linspace(0,1,sample_points)))
    else:
        print(type(obj))
    return np.array(path)

print(svg_attributes['viewBox'])
print(paths)
for p in paths:
    arr = svgpathtools_unpacker(p)
    points = np.array([[num.real, num.imag] for num in arr])
    # print(points)
print(points)
tri = spatial.Delaunay(points)
# print(tri.simplices)

# plt.triplot(points[:,0], points[:,1], tri.simplices)
# plt.plot(points[:,0], points[:,1], 'o')
# plt.show()