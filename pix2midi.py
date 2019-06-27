from PIL import Image

from midiutil import MIDIFile


image_file = Image.open("tu2.png") # open colour image


# resize image
width, height = image_file.size
if width >= height:
    ratio = width/height
    height = 88
    width = int(height*ratio)
    image_file = image_file.rotate(90, expand=True)
    image_file.save('result_roated.png')
else:
    ratio = height/width
    height = 88
    width = int(height*ratio)
    image_file.save('result_roated.png')

image_file = image_file.resize((height, width), Image.ANTIALIAS)
image_file = image_file.convert('1') # convert image to black and white


track    = 0
channel  = 0
time     = 0    # In beats
duration = 0.1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard
min_midi = 21
# max_midi = 109  # 88+21
MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

# itter over pixels - height and widht changed and are the opposide now
for y in range(width):
    for x in range(height):
        pixel = image_file.getpixel((x, y))
        if pixel <= 150:
            MyMIDI.addNote(track, channel, min_midi + x, time + (duration*(width - y)), duration, volume)

with open("toad.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

image_file.save('result.png')
