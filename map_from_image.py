from PIL import Image
try:
    im = Image.open("map.jpg")
except:
    im = Image.open('map.png')
f = open('map.txt', mode='w')
pixels = im.load()
x, y = im.size
current_line = ''
for i in range(y):
    for j in range(x):
        r, g, b = pixels[j, i]
        if not r and not g and not b:
            current_line += '1'
        else:
            current_line += '0'
    f.write(current_line)
    f.write('\n')
    current_line = ''
f.close()


