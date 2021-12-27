import pickle

from Controllers.CamerController import CV2Controller
cam = CV2Controller()

data = list()
for i in range(50):
    pic, _ = cam.takePicture()
    data.append(pic)

folderPath = "TestFiles/"
print("input filename")
name = input()
path = folderPath + name + ".pckl"
with open(path, "wb") as f:
    pickle.dump(data, f)
    f.close()