import Image

im = Image.open('C:/Users/Public/Pictures/Sample Pictures/power.jpg');
w,h=im.size;

im.thumbnail((w/2,h/2))
im.save('C:/Users/Public/Pictures/Sample Pictures/thumbnail.jpg')

imf=im.filter(ImageFilter.BLUR)





