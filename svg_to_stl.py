from subprocess import call

script = '''resize(newsize=[{},{},{}])
    linear_extrude(height = 5, center = true, scale=1)
        import(file = "/Users/tahlia/Downloads/frontback.svg", center = true, dpi = 96);
'''

def makeSVGScript(x, y, z):
    formatted_script = script.format(x, y, z)
    nameFile = 'script.scad'
    file = open(nameFile, 'w')
    file.write(formatted_script)
    file.close()

print('processing file')
makeSVGScript(100,100,2)
# get dimensions
stlName = 'out.stl'
stlNamePath = 'script.scad'
call(['openscad', '-o', stlName, stlNamePath])
print('Completed')