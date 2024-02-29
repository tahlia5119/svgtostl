from subprocess import call
import svgpathtools  as spt
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt


script = '''
use <voronoi.scad>

point_set = [
    {}
];

resize(newsize=[100,100,2])
    linear_extrude(height = 5)
        difference() {{
            import(file = "test.svg", center = true, dpi = 300);
            voronoi(points = point_set, L = {puttheradiushereMaxyorxabsaftercentring}, thickness = 10, nuclei = false);
        }}
'''

def parse_array(np_arr):
    string = ''
    for i, a in enumerate(np_arr):
        x = int(round(a[0]))
        y = int(round(a[1]))
        string += f'[{x}, {y}]'
        if i != len(np_arr)-1:
            string += ',\n'
    return string

def makeSVGScript(points):
    formatted_script = script.format(points)
    nameFile = 'script_voronoi_created.scad'
    file = open(nameFile, 'w')
    file.write(formatted_script)
    file.close()

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

def centre_points(points):
    x_points = [p[0] for p in points]
    y_points = [p[1] for p in points]
    
    max_x = max(x_points)
    min_x = min(x_points)
    max_y = max(y_points)
    min_y = min(y_points)

    print(f'{max_x}, {max_y}, {min_x}, {min_y}')

    x_offset = abs((min_x + max_x)/2)
    y_offset = abs((min_y + max_y)/2)

    print(f'{x_offset}, {y_offset}')

    centred_points = [[p[0]-x_offset, p[1]-y_offset] for p in points]

    return np.array(centred_points)

print('processing file')

# print('extracting svg points')
# svg_paths, attributes, svg_attributes = spt.svg2paths2('test.svg')
# for p in svg_paths:
#     arr = svgpathtools_unpacker(p)
#     ext_points = np.array([[num.real, num.imag] for num in arr])

# print('creating svg script')
# makeSVGScript(parse_array(centre_points(ext_points)))

print('creating stl')
stlName = 'out_voronoi.stl'
stlNamePath = 'script_voronoi_created.scad'
call(['openscad', '-o', stlName, stlNamePath])
print('Completed')



# tri = spatial.Delaunay(points)