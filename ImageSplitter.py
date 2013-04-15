import time
import hashlib
import Image
import os


class ImageSplitter:
    im = None
    __splitImage = []
    __splitImageBaseName = ''
    
    def __init__(self, filepath):
        self.im = Image.open(filepath)
        #self.width, self.height = self.im.size
        #print self.width, self.height

    def __CalcNewImageSize(self, hpart, wpart):
        width, height = self.im.size
        if height > width:
            nheight = 48 * hpart
            nwidth  = (nheight*width)/height
        else:
            nwidth  = 48 * wpart
            nheight = (nwidth*height)/width

        #print nwidth, nheight
        return nwidth, nheight
    @classmethod
    def uniqid(cls):
        m = hashlib.md5( str(time.time()) )
        return m.hexdigest()
    
    def split(self, hpart = 3, wpart = 3):
        #hpart, wpart = 3, 3
        nwidth, nheight = self.__CalcNewImageSize(hpart, wpart)
        nim = self.im.resize( (nwidth, nheight) )
        pheight, pwidth = nheight/hpart, nwidth/wpart


        
        uid = ImageSplitter.uniqid()
        pim_fname = uid+'_%dx%d.jpg'
        images = []
        #count = 0
        for i in range(0, wpart):
            for j in range(0, hpart ):
                #count = count+1
                pim = nim.crop( (i*pwidth, j*pheight, (i+1)*pwidth, (j+1)*pheight) )
                #name = pim_fname % (i+j*wpart)
                fname = pim_fname % (j, i)
                #print name, i, j
                #pim.save(name, 'jpeg')
                images.append( {'file':pim, 'name':fname} )
        
        self.__splitImage = images
        self.__splitImageBaseName = uid
        return self.__splitImage, self.__splitImageBaseName
    
    def SaveAllImage(self, path):
        #print self.__splitImage
        path = os.path.join(path, self.__splitImageBaseName)
        if not os.path.isdir(path):
            os.mkdir(path)
        for img in self.__splitImage:
            img['file'].save(os.path.join(path, img['name']), "JPEG", quality=100)
        

if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__name__))[0];
    imgSplit = ImageSplitter('12345.jpg')
    s, b = imgSplit.split()
    imgSplit.SaveAllImage(path)

    #print ImageSplitter.uniqid()
