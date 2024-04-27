from PNG import PNG

test = PNG("images/image7.png")
test.showPLTE()
test.fourierTransform()
test.mergeIDAT()
test.printData()
test.saveFile("images/test.png")    
