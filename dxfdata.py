class DXFData(object):

    def __init__(self, posX, posY, posZ, svgCode, svgType):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ

        self.svgCode = svgCode
        self.svgType = svgType

    def getPosition(self):
        tempList = [self.posX,self.posY,self.posZ]
        return tempList

    def getCode(self):
        return self.svgCode

    def getType(self):
        return self.svgType    