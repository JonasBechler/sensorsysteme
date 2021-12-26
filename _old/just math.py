import math


def function(*args, **kwargs):
    for i, arg in enumerate(args):
        print(arg)

    for kw in kwargs:
        if kw == "i":
            print(kwargs[kw])
        if kw == "time":
            print(kwargs[kw])
        if kw == "pos":
            print(kw)
            print(kwargs[kw][0:2])
    print("Hallllllo")

def calc():
    z_real_soll = 4  # mm
    z_real_ist = 3.5  # mm

    steps_ist = 800
    steps_soll = z_real_soll / z_real_ist * steps_ist
    print(steps_soll)





if __name__ == '__main__':
    hyp = 189
    angle = 15/360*math.pi
    math.cos(angle)*hyp
