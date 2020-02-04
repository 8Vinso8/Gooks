from PIL import Image
try:
    im = Image.open("data/map.jpg")
except FileNotFoundError:
    im = Image.open('data/map.png')
f = open('data/map.txt', mode='w')
pixels = im.load()
x, y = im.size
current_line = ''
for i in range(y):
    for j in range(x):
        r, g, b = pixels[j, i]
        if not (r or g or b):
            current_line += '1'
        else:
            current_line += '0'
    f.write(current_line)
    f.write('\n')
    current_line = ''
f.close()


