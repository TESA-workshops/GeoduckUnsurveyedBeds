from numpy.random import normal,shuffle
from numpy import ndarray, array
from wchNorm import InvNorm

class LowHalfNormal():
    def __init__(self,mu,sigma):
        self.mu=mu
        self.sigma=sigma

    def rvs(self,n=None,equiProb=False):
        if self.sigma<1.e-6:
            if n==None:return(self.mu)
            return(array(n*[self.mu]))
        if not(equiProb):
            z1=-abs(normal(0,self.sigma,size=n))
            z2=z1+self.mu
            return(z2)
        p=list(map(lambda i:(i+.5)/n,range(n)))
        result=self.isf(p)
        shuffle(result)
        return(result)
              

    def isf(self,p):
        if isinstance(p,(list,ndarray)):
            z=list(map(lambda t:self.mu+self.sigma*InvNorm(1-t/2),p))
            if isinstance(p,ndarray):z=array(z)
            return(z)
        else:
            z=self.mu+self.sigma*InvNorm(1-p/2)
            return(z)



if __name__ == "__main__":
    mu=0
    sigma=1
    LHN=LowHalfNormal(mu,sigma)
    print('\n')
    for i in range(10):print(LHN.rvs())
    print('\n')

    print('\n')
    print(LHN.isf([.05,.10]))
    print(LHN.isf(.05),LHN.isf(.10) )
    from matplotlib import pyplot as plt
    x1=LHN.rvs(1000)
    x2=LHN.rvs(1000,equiProb=True)
    x3=LHN.rvs(1000,equiProb=True)
    y2=sorted(x2)
    y3=sorted(x3)
    plt.plot(y2,y3)
    #plt.hist(x1,fc='r',alpha=0.2)
    #plt.hist(x2,fc='b',alpha=0.2)
    #plt.hist(x3,fc='k',alpha=0.2)
    plt.show()

    print('\n')
    print(LHN.isf([.0125,.025]))
