# import cv2, numpy, wx, os, platform
from PIL.Image import open
from os import system as os_sys
from platform import system as plf_sys
from wx import App, Frame, ID_ANY, FileDialog, FD_OPEN, FD_FILE_MUST_EXIST

def processImg(outputType = 0, filepath = '', BlackWriteLine = 200):
    
    img = open(filepath)
    try:
        img = img.convert('RGB')
        newimg = []

        process = 0
        for i in range(img.width):
            newimg.append([])
            if( i/img.height>=process/10 ):
                print(process*10, '%')
                process+=1


            for j in range(img.height):
                coord = i, j
                newimg[len(newimg)-1].append([])
                cur = 0
                r, g, b = img.getpixel(coord)
                cur = r+g+b
                if outputType==1:
                    for k in range(3):
                        color = ta, tb, tc = int(cur/3), int(cur/3), int(cur/3)
                        img.putpixel(coord, color)
                elif outputType==2:
                    if cur/3>BlackWriteLine:
                        for k in range(3):
                            color = ta, tb, tc = 255, 255, 255    
                            img.putpixel(coord, color)
                    else:
                        for k in range(3):
                            color = ta, tb, tc = 0, 0, 0
                            img.putpixel(coord, color)
                

        print('100%')
        print('Saving Image...')
        img.save('output{}.png'.format(BlackWriteLine))

    finally:
        img.close()
        
    if plf_sys() == 'Windows':
        os_sys('start {}'.format('output{}.png'.format(BlackWriteLine)))

    print('Done')

app = App()
frame = Frame(
    parent=None,
    id=ID_ANY,
    title='Dogs vs Cats'
)

openFileDialog = FileDialog(frame, "Open", "", "", 
                                "All files (*)|*.*|" "JPG (*.jpg)|*.jpg|" "PNG (*.png)|*.png" , 
                                FD_OPEN | FD_FILE_MUST_EXIST)
openFileDialog.ShowModal()
filename = openFileDialog.GetPath()
openFileDialog.Destroy()

outputType = -1
while outputType<1 or outputType>2:
    try:
        outputType = int(input(
            '1. Transfer to Grayscale.\n' +
            '2. Transfer to "only black and write" image\n' + 
            '>> '
        ).split('.')[0])
    except ValueError:
        outputType = -1

BlackWriteLine = -1
if outputType==2:
    while BlackWriteLine <0:
        try:
            BlackWriteLine = int(input(
                'How dark for your image?  (0~255, Suggest: {})\n'.format('150~200') + 
                '>> '
            ))
        except ValueError:
            BlackWriteLine = -1
    
else:
    BlackWriteLine = 200

processImg(outputType, filename, BlackWriteLine)
