def save(ctx, name):
    for i in range(len(ctx.objects)):
        ctx.objects[i].uid = i #Gives objects IDs for easier loading

    with open(f"saves/{name}.txt", "w") as f:
        for i in ctx.objects:
            match i.objid: #Writes all objects to file in text form
                case 0:
                    f.write(stringconvert([i.uid, i.objid, i.radius, i.x, i.y, i.dx, i.dy, i.ax, i.ay, i.mass, i.drawtrail, i.static]) + "\n")
                case 1:
                    f.write(stringconvert([i.uid, i.objid, i.x, i.y, i.angle, i.sizex, i.sizey, i.spinvel]) + "\n")
                case 2:
                    f.write(stringconvert([i.uid, i.objid, i.p1[0], i.p1[1], i.p2[0], i.p2[1]]) + "\n")
                case 3: #Children need extra formatting
                    f.write(stringconvert([i.uid, i.objid, i.x, i.y, i.angle, i.spinvel, f"[{returnchildren(i)}]"]) + "\n")


def load(ctx, name, objs):
    circle, square, line, empty = objs[0], objs[1], objs[2], objs[3] #Classes for instantiating
    circles, squares, lines, empties = [],[],[],[]
    children = []
    try: #Ensure files exist
        f = open(f"saves/{name}.txt", "r").read()
    except:
        return

    objectstemp = f.split("\n") #List of object strings
    objectstemp = objectstemp[:-1] #Remove trailing entry
    objects = []
    for i in objectstemp:
        objects.append(i.split(",")) #List of objects in text form, attributes separated

    for i in range(len(objects)):
        for j in range(len(objects[i])):
            if j > 0:
                try:
                    objects[i][j] = float(objects[i][j]) #Converts necessary attributes to floats
                except:
                    pass

    for i in objects:
        if int(i[1]) == 0: #Instantiate new circle
            new = circle(i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], True if i[10] == "True" else False, True if i[11] == "True" else False)
            new.uid = i[0]
            circles += [new]
        elif int(i[1]) == 1: #Instantiate new square
            new = square(i[2], i[3], i[4], i[5], i[6], i[7])
            new.uid = i[0]
            squares += [new]
        elif int(i[1]) == 2: #Instantiate new line
            new = line((i[2], i[3]), (i[4], i[5]))
            new.uid = i[0]
            lines += [new]
        else: #Instantiate new empty
            new = empty(i[2], i[3], i[4], i[5], [])
            children.append(reverselist(i[6]))
            new.uid = i[0]
            empties += [new]

    objects = circles + squares + lines + empties #Final objects list
    uids = list(i.uid for i in objects)

    for i in range(len(children)): #Cycles through list of children to set empty children to relative objects
        for j in children[i]:
            if j != "":
                empties[i].children.append(objects[uids.index(j)])

    ctx.balls, ctx.squares, ctx.lines, ctx.empties = circles, squares, lines, empties #Final loading
    ctx.objects = objects


def reverselist(string): #Reverses list and splits into children IDs
    return string[1:-1].split("~")

def stringconvert(list): #Converts list to string, no square brackets or trailing comma
    out = ""
    for i in list:
        out += str(i)
        out += ","
    return out[:-1]

def returnchildren(object): #Returns string of children IDs, separated by tildes
    out = ""
    for i in object.children:
        out += str(i.uid)
        out += "~"
    return out[:-1]
