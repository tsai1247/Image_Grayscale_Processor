# import cv2, numpy, wx, os, platform
from cv2 import imread, imwrite
from os import system as os_sys
from platform import system as plf_sys
from wx import App, Frame, ID_ANY, FileDialog, FD_OPEN, FD_FILE_MUST_EXIST
from numpy import array as nparr

def processImg(outputType = 0, filepath = '', BlackWriteLine = 200):
    img = imread(filepath)
    print('Image size:', img.shape)

    newimg = []

    process = 0
    for i in range(len(img)):
        newimg.append([])
        if( i/len(img)>=process/10 ):
            print(process*10, '%')
            process+=1


        for j in range(len(img[i])):
            newimg[len(newimg)-1].append([])
            cur = 0
            for k in range(len(img[i, j])):
                cur += img[i, j, k]
            if outputType==1:
                for k in range(3):        
                    newimg[len(newimg)-1][ len(newimg[len(newimg)-1])-1 ].append(int(cur/3))          
            elif outputType==2:
                if cur/3>BlackWriteLine:
                    for k in range(3):        
                        newimg[len(newimg)-1][ len(newimg[len(newimg)-1])-1 ].append(255)
                else:
                    for k in range(3):
                        newimg[len(newimg)-1][ len(newimg[len(newimg)-1])-1 ].append(0)
            

    print('100%')
    print('Saving Image...')

    imwrite('output{}.png'.format(BlackWriteLine), nparr(newimg))

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
