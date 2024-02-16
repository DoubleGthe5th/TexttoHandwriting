"""
Meant to take handwritten data and convert to letter format
"""
import random
import PIL
from PIL import Image

#opens letter database 
letters = open('A_Z Handwritten Data.csv')
letters = letters.readlines()
letters = [l.replace('\n','') for l in letters]
print("Data gotten")
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#creates list of random letters
found = False
while not found:
    l = random.randint(0,len(letters))
    try:
        letter = int(letters[l][0:2])
    except:
        letter = int(letters[l][0:1])
    if len(alphabet[letter]) == 1:
        alphabet[letter] = [int(ele) for ele in letters[l].split(',')]
        alphabet[letter].pop(0)
    found = True
    for x in range(26):
        if len(alphabet[x]) == 1:
            found = False
            break
#creates list of images
images = []
for letter in alphabet:
    im = PIL.Image.new(mode="RGB", size=(28, 28))
    pixels = im.load()
    for x in range(784):
        pixels[(x%28),((x-x%28)/28)] = (255-letter[x],255-letter[x],255-letter[x])
    images.append(im)
images[0].show()
#sets page to be printed
height = 11
width = 8.5
line_spacing = 9/32.0
lines = 33
side_margins = 11/8

#makes blank page
pixel_size = line_spacing/28
final_page = PIL.Image.new(mode="RGB",size=(int(width/pixel_size),int(height/pixel_size)),color=(255,255,255))
formatted_page = final_page
pixels = formatted_page.load()
#gathers textual data
data = open('data.txt','r')
data = data.read()
words = data.split()
pixels_left = formatted_page.width-2*int(side_margins/width*formatted_page.width)
lines_left = lines
word = 0
while lines_left > 0:
    if len(words[word])*28 < pixels_left:
        h = formatted_page.height - 28*lines_left
        w = formatted_page.width-int(side_margins/width*formatted_page.width) - pixels_left
        for letter in words[word]:
            for x in range(28):
                for y in range(28):
                    pixels[w+x,h+y] = images[ord(letter)-65].getpixel((x,y))
            w += 28
            pixels_left -= 28
        if pixels_left >= 28:
            for x in range(28):
                for y in range(28):
                    pixels[w+x,h+y] = (255,255,255)
            w += 28
            pixels_left -= 28           
        word += 1
        if word == len(words):
            break
    else:
        pixels_left = formatted_page.width-2*int(side_margins/width*formatted_page.width)
        lines_left -= 1
#creates formatted page
w = formatted_page.height
written_lines = 0
while written_lines < lines:
    w -= 28
    for y in range(formatted_page.width):
        pixels[y,w] = (0,0,255)
    written_lines+=1
for y in range(formatted_page.height):
    pixels[int(side_margins/width*formatted_page.width),y] = (255,0,0)
for y in range(formatted_page.height):
    pixels[formatted_page.width-int(side_margins/width*formatted_page.width),y] = (255,0,0)
unformatted_pixels = final_page.load()
formatted_page.show()
