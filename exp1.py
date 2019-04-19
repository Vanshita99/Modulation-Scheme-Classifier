
import matplotlib
import matlab.engine

eng=matlab.engine.start_matlab()
v,w,x,BW,z=eng.testFunction(nargout=5)
print(v)

