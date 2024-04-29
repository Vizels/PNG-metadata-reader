from PNG import PNG

test = PNG("images/image5.png")
test.merge_IDAT()
test.printData()
test.show_PLTE()
test.fourierTransform()
# test.saveFile("images/test.png")   
