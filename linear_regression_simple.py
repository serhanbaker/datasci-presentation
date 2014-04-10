from pylab import *
x = [0.2, 1.3, 2.1, 2.9, 3.3]
y = [3.3, 3.9, 4.8, 8.5, 6.9]

"""
Polyfit takes two variables and a degree. 
1 for a linear function. 
m (for the slope) and b for the y-intercept of the equation y = mx + b.
"""
(m, b) = polyfit(x, y, 1)
print b
print m

yp = polyval([m, b], x) # for the graph

plot(x, yp)
scatter(x,y)
grid(True)
xlabel('x')
ylabel('y')
show()