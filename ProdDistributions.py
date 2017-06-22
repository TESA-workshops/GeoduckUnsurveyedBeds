from norm import norm
from LowHalfNormal import LowHalfNormal
from mquantiles import mquantiles
from numpy import array,ndarray
import pdb

class ProdDistributions():
    '''Represent a product of two distributions as an array of equiprobable values.
    Initial distributions have a .isf function (scipy.stats)'''

    def __init__(self, dist1, dist2,n=100,p=None):
        if dist1==[]:
            self.value=[]
            return
        if dist2==[]:
            self.value=[]
            return
        self.n=n
        self.p=p
        if self.p==None:self.p=list(map(lambda t:(t+.5)/self.n,range(self.n)))
        self.n=len(self.p)
        if isinstance(dist1,(list,ndarray)):eqpv1=array(dist1)
        else:
            eqpv1=dist1.isf(self.p)
        if isinstance(dist2,(list,ndarray)):eqpv2=array(dist2)
        else:
            eqpv2=dist2.isf(self.p)

        n1,n2=len( eqpv1),len(eqpv2)
        equiProb=array(eqpv1).reshape(n1,1)*array(eqpv2)#matrix multiplication to get a equiprobable value
        try:
            equiProb=equiProb.reshape(1,n1*n2)[0]
        except:
            pdb.set_trace()
            equiProb=equiProb.reshape(1,n1*n2)[0]
        try:
            self.value=mquantiles(equiProb,self.p)
        except:
            self.value=list(map(lambda x:-1,self.p))


    def isf(self,p=None,n=None):
        if p==None:
            if n==None:
                return(self.value)
            else:
                p=list(map(lambda t: (t+.5)/n,range(n)))
        if self.value==[]:return(list(map(lambda x:-1,p)))
        result=mquantiles(self.value,p)
        return(result)

    

if __name__ == "__main__":
    from norm import norm
    from LowHalfNormal import LowHalfNormal
    p=[.0005,.005,.05,.15,.25,.35,.45,.55,.65,.75,.85,.95,.995,.9995]
    test1=LowHalfNormal(10,1)
    test2=norm(20,2)
    test3=array(range(10))

    test4=ProdDistributions(test1,test2)
    print( 'test4.isf(n=3) ', test4.isf(n=10))

    test5=ProdDistributions(test4,test3)
    print( 'test5.isf(n=10) ', test5.isf(n=10))
