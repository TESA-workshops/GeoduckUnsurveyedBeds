from scipy.stats import norm
from scipy.stats.mstats import mquantiles
from numpy.random import choice,seed
from numpy import array

seed(756)
Den=[ 0.08015092,  0.10789958,  0.12167541,  0.21219431,  0.07920235,  0.19467892,  0.5431346,   0.13779066]

MnWgt=norm(2.804086007439/2.2,0.02273154621778/2.2)

class BedArea():
 def __init__(self,mu,sigma):
     self.mu=mu
     self.sigma=sigma
     self.nsource=norm(0,1)
 def rvs(self,size=None):
      z=self.nsource.rvs(size=size)
      result=self.mu+self.sigma*z
      return(result)
BA=BedArea(26.902999877929*10000,26.902999877929*1000)
def RandDen(n):
    result=choice(array(Den),size=n,replace=True)
    return(result)

p=[.005,.025,.05,.125,.5,.875,.95,975,.995]
p=[.125,.5,.875]
n=10000

B=BA.rvs(size=n)*MnWgt.rvs(size=n)* RandDen(n)
#print(B)
print(mquantiles(B,p))

      
      
