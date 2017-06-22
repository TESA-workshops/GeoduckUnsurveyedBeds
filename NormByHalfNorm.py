from norm import norm
from LowHalfNormal import LowHalfNormal
from mquantiles import mquantiles
from numpy import array
import pdb

class NormByHalfNorm:
    def __init__(self,mux=0,sigmax=1,muh=0,sigmah=1,n=100):
        self.mux=mux
        self.sigmax=sigmax
        self.muh=muh
        self.sigmah=sigmah
        self.n=n
        p=list(map(lambda t:(t+.5)/self.n,range(self.n)))

        normx=norm(self.mux,self.sigmax)
        normh=LowHalfNormal(self.muh,self.sigmah)

        EquiProbx=array(normx.isf(p))
        EquiProbh=array(normh.isf(p))
        EquiProb=EquiProbx.reshape(n,1)*EquiProbh
        self.EquiProb=EquiProb.reshape(1,n*n)[0]

    def isf(self,p=None,n=None):
        if p==None:
            if n==None:n=self.n
            p=list(map(lambda t:(t+.5)/n,range(n)))
        result=mquantiles(self.EquiProb,prob=p)
        return(result)

class ProdEquiProb:
    def __init(self,x1,x2,n=None):
        '''ProdEquiProb(x1,x2,n=None)
        x1 and x2 are both arrays representing equally probable values from two distributions.
        n is the number of values to use to represent distribution of product.
          Default is to use the longest of len(x1) and len(x2)'''

        y1=array(x1)
        if isinstance(x1,(list,ndarray)):y1=array([x1])
        if isinstance(x2,(list,ndarray)):y2=array([x2])
        n1=len(y1)
        n2=len(y2)
        if n==None:n=max([n1,n2])
        self.p=list(map(lambda t: (t+.5)/n,range(n)))
        if n1==1:
            self.EPV=x1*y2
        elif n2==1:
            self.EPV=x2*y1
        else:
            t1=y1.reshape(n1,1)*y2
            t2=t1.reshape(1,n1*n2)
            p=list(map(lambda t: (t+.5)/n,range(n)))
            self.EPV=mquantiles(t2,prob=p)

    def isf(self,p=None,n=None):
        if p==None:
            if n==None:n=self.n
            p=list(map(lambda t:(t+.5)/n,range(n)))
        result=mquantiles(self.EPV,prob=p)
        return(result)
            
        

            
                

if __name__ == "__main__":

    test1=NormByHalfNorm(mux=20,sigmax=2,muh=10,sigmah=1)
    p=[.0005,.005,.05,.15,.25,.35,.45,.55,.65,.75,.85,.95,.995,.9995]

    #print( '\n  test1.isf(p) ' ,test1.isf(p=p) )
    print( '\n  test1.isf(p) ' ,test1.isf(n=10) )
    

