from PIL import Image

class Slicer():
    def slice(image, width, height):
        image_path = "../../images"
        PARKING_SPOTS = [(), (), (), (), (), (), (), (), (), (), (), (), (), ()]
        LOT_IMAGE = Image.open(image_path)
        subimage = 0
        for i in range(0, 14):
            a = LOT_IMAGE.crop(PARKING_SPOTS[i][1], PARKING_SPOTS[i][2]) # how to make a good box out of two pixels?
            a.save(str(PARKING_SPOTS[i][0]) + '.png')




