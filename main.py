from PNG import PNG

test = PNG("images/test.png")
test.mergeIDAT()
test.printData()
# test.showPLTE()
# test.fourierTransform()
test.saveFile("images/test.png")   
