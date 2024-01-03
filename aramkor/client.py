import sys,json

with open(sys.argv[1]) as f:
    data = json.load(f)

end_points = data["end-points"]
switches = data["switches"]
pc = sorted(data["possible-circuits"],key = len)
weights = {tuple((pc["points"])) : pc["capacity"] for pc in data["links"]}
duration = data["simulation"]["duration"]
demands = data["simulation"]["demands"]
nodes = end_points + switches
allocated = []
allocatedPC = []
def all_edges(c):
    return list(zip(c,c[1:]))

def allocate(demand,init,aim):
    for circuit in pc:
        if ((init == circuit[0] and aim == circuit[-1]) and (all (weights[edge] >= demand["demand"] for edge in all_edges(circuit)))):
            for e in all_edges(circuit):
                weights[e] = weights[e] - demand["demand"]
                allocated.append(e)
            allocatedPC.append(circuit)
            return True
    return False

def deallocate(demand,init,aim):
    for a in pc:
        if a is not None:
            if(init == a[0] and aim == a[-1]):
                for e in all_edges(a):
                    weights[e] = weights[e] + demand["demand"]
                    if(e in allocated):
                        allocated.remove(e)
                if(a in allocatedPC):
                    allocatedPC.remove(a)
                    return True
                else:
                    return False
    return False


def simulation():
    db = 1
    for time in range(1,duration+1):
        for num,demand in enumerate(demands):
            if(time == demand["start-time"]):
                if(allocate(demand,demand["end-points"][0],demand["end-points"][1])):
                    print("%d. igény foglalás: %s<->%s st:%d - sikeres" %(db,demand["end-points"][0],demand["end-points"][1],time))
                else:
                    print("%d. igény foglalás: %s<->%s st:%d - sikertelen" %(db,demand["end-points"][0],demand["end-points"][1],time))
                db = db + 1
            elif(time == demand["end-time"]):
                if(deallocate(demand,demand["end-points"][0],demand["end-points"][1])):
                    print("%d. igény felszabadítás: %s<->%s st:%d" %(db,demand["end-points"][0],demand["end-points"][1],time))
                db = db + 1

def main():
    simulation()

if __name__ == "__main__":
    main()