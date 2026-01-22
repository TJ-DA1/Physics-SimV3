from uuid import uuid4

def save(ctx, name):
    emptieslist = list(ctx.empties)
    orderedemptieslist = []

    for i in ctx.objects:
        i.uuid = str(uuid4())
    with open(f"saves/{name}.txt", "w") as f:
        for i in ctx.objects:
            match i.objid:
                case 0:
                    f.write(stringconvert([i.uuid, i.objid, i.radius, i.x, i.y, i.dx, i.dy, i.ax, i.ay, i.mass, i.drawtrail, i.static]) + "\n")
                case 1:
                    f.write(stringconvert([i.uuid, i.objid, i.x, i.y, i.angle, i.sizex, i.sizey, i.spinvel]) + "\n")
                case 2:
                    f.write(stringconvert([i.uuid, i.objid, i.p1[0], i.p1[1], i.p2[0], i.p2[1]]) + "\n")
                case 3:
                    f.write(stringconvert([i.uuid, i.objid, i.x, i.y, i.angle, i.spinvel, f"[{returnchildren(i)}]"]) + "\n")


def load(ctx, name, objs):
    circle, square, line, empty = objs[0], objs[1], objs[2], objs[3]
    circles, squares, lines, empties = [],[],[],[]
    children = []
    f = open(f"saves/{name}.txt", "r").read()
    objectstemp = f.split("\n")
    objectstemp = objectstemp[:-1]
    objects = []
    for i in objectstemp:
        objects.append(i.split(","))

    for i in range(len(objects)):
        for j in range(len(objects[i])):
            if j > 0:
                try:
                    objects[i][j] = float(objects[i][j])
                except:
                    pass
    for i in objects:
        print(i)
    for i in objects:
        if int(i[1]) == 0:
            new = circle(i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], True if i[10] == "True" else False, True if i[11] == "True" else False)
            new.uuid = i[0]
            circles += [new]
        elif int(i[1]) == 1:
            new = square(i[2], i[3], i[4], i[5], i[6], i[7])
            new.uuid = i[0]
            squares += [new]
        elif int(i[1]) == 2:
            new = line((i[2], i[3]), (i[4], i[5]))
            new.uuid = i[0]
            lines += [new]
        else:
            new = empty(i[2], i[3], i[4], i[5], [])
            children.append(reverselist(i[6]))
            new.uuid = i[0]
            empties += [new]

    objects = circles + squares + lines + empties
    uuids = list(i.uuid for i in objects)

    for i in range(len(children)):
        for j in children[i]:
            if j != "":
                empties[i].children.append(objects[uuids.index(j)])

    ctx.balls, ctx.squares, ctx.lines, ctx.empties = circles, squares, lines, empties
    ctx.objects = objects


def reverselist(string):
    return string[1:-1].split("~")

def stringconvert(list):
    out = ""
    for i in list:
        out += str(i)
        out += ","
    return out[:-1]

def returnchildren(object):
    out = ""
    for i in object.children:
        out += str(i.uuid)
        out += "~"
    return out[:-1]

def booleanevaluate(list):
    ret = True
    for i in list:
        if i == False:
            ret = False
    return ret