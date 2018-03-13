from norm import norm
from mquantiles import mquantiles
from numpy import array
import pdb

class ProdNorm:
    def __init__(self,mux=0,sigmax=1,muy=0,sigmay=1,n=100):
        self.mux=mux
        self.sigmax=sigmax
        self.muy=muy
        self.sigmay=sigmay
        self.n=n
        p=list(map(lambda t:(t+.5)/self.n,range(self.n)))

        normx=norm(self.mux,self.sigmax)
        normy=norm(self.muy,self.sigmay)

        EquiProbx=array(normx.isf(p))
        EquiProby=array(normy.isf(p))
        EquiProb=EquiProbx.reshape(n,1)*EquiProby
        self.EquiProb=EquiProb.reshape(1,n*n)[0]

    def isf(self,p=None,n=None):
        if p==None:
            if n==None:n=self.n
            p=list(map(lambda t:(t+.5)/n,range(n)))
        result=mquantiles(self.EquiProb,prob=p)
        return(result)

if __name__ == "__main__":

    test1=ProdNorm(mux=10,sigmax=1,muy=20,sigmay=2,n=10)
    test2=ProdNorm(mux=10,sigmax=1,muy=20,sigmay=2,n=100)
    test3=ProdNorm(mux=10,sigmax=1,muy=20,sigmay=2,n=400)
    p=[.0005,.005,.05,.15,.25,.35,.45,.55,.65,.75,.85,.95,.995,.9995]

    print( '\n  test1.isf(p) ' ,test1.isf(p) )
    print( '\n  test2.isf(p) ' ,test2.isf(p) )
    print( '\n  test3.isf(p) ' ,test3.isf(p) )

