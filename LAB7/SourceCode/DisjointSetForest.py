# Implementation of disjoint set forest (or union/find data structure)
# Programmed by Olac Fuentes
# Last modified November 13, 2019

from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import graph_AL as al
import graph_AM as am
import graph_EL as el

class DSF:
    # Constructor
    def __init__(self, sets):
        # Creates forest with 'sets' root nodes
        self.parent = np.zeros(sets,dtype=int)-1
      
#    def find(self,i):
#        # Returns root of tree that i belongs to
#        if self.parent[i]<0:
#            return i
#        return self.find(self.parent[i])
        
    def find(self, i):
        if self.parent[i] < 0:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self,i,j):
        # Makes root of j's tree point to root of i's tree if they are different
        # Return 1 if a parent reference was changed, 0 otherwise
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_j] = root_i
            return 1
        return 0 
    
    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(self.parent)):
            if self.parent[i]<0:
                ax.plot([i*scale,i*scale],[0,scale],linewidth=1,color='k')
                ax.plot([i*scale-1,i*scale,i*scale+1],[scale-2,scale,scale-2],linewidth=1,color='k')
            else:
                x = np.linspace(i*scale,self.parent[i]*scale)
                x0 = np.linspace(i*scale,self.parent[i]*scale,num=5)
                diff = np.abs(self.parent[i]-i)
                if diff == 1:
                    y0 = [0,0,0,0,0]
                else:
                    y0 = [0,-6*diff,-8*diff,-6*diff,0]
                f = interp1d(x0, y0, kind='cubic')
                y = f(x)
                ax.plot(x,y,linewidth=1,color='k')
                ax.plot([x0[2]+2*np.sign(i-self.parent[i]),x0[2],x0[2]+2*np.sign(i-self.parent[i])],[y0[2]-1,y0[2],y0[2]+1],linewidth=1,color='k')
            ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
             bbox=dict(facecolor='w',boxstyle="circle"))
        ax.axis('off') 
        ax.set_aspect(1.0)
        
        
    def edges_to_disjoint_set_forest(self, subset_of_edges):
        for bucket in subset_of_edges:
            for edge in bucket:
                self.union(edge[0], edge[1])