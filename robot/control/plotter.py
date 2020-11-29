from Communication import Network
import matplotlib.pyplot as plt
import Commands as coms
import numpy as np



# while True:
    # print(sub.listen())




class point():
    def __init__(self,r,ang):
        self.r = r
        self.ang = ang
    def comp_ang(self,value):
        return self.ang == value

class plotter():
    def __init__(self):
        self.ax = plt.subplot(111,projection='polar')
        self._as = [0]
        self._rs = [0]
        self.points = [point(0,0)]
        self._pl, = self.ax.plot(self._as,self._rs,'*')
        self.ax.set_ylim(0,4)
        self.plot()
    def new_point(self,r,ang):

        for p in self.points:
            if p.comp_ang(ang):
                self.points.remove(p)
                break
        self.points.append(point(r,ang))
        self.plot()

    def make_lists(self):
        self._as = []
        self._rs = []
        for p in self.points:
            self._as.append(p.ang)
            self._rs.append(p.r)

    def plot(self):
        self.make_lists()
        self._pl.set_data(self._as,self._rs)
        plt.pause(0.00001)
        
        

sub = Network(subscribtions=coms.get_plotter_subs())
sub.setuplistner()
running = True
plot = plotter()
while running:
    command = sub.listen()
    if command == coms.shutdown():
        running = False
    else:
        d = coms.decoder(command)
        if d[0] > 0.05:
            plot.new_point(d[0],d[1])
            
                

# plt.savefig('scatter.png')
                
                


# plt.savefig('scatter.png')