import numpy as np 
import matplotlib.pyplot as plt
from scipy.linalg import solve

A = np.array([[2, 3],
            [1, -1]])

b = np.array([7, 1])

x = solve(A, b)
print(x)

x_values = np.linspace(-5, 5, 100)
y1 = ( 7 - 2 * x_values ) /3
y2 = x_values - 1

plt.plot(x_values, y1, label ='2x + 3y = 7')
plt.plot(x_values, y2, label ='x -y = 1')
plt.scatter(x[0], x[1], color = 'red', label = 'Nghiem')
plt.xlabel('x')
plt.xlabel('y')
plt.title('giai he phuong trinh bac nhat 2 an')
plt.legend()
plt.grid(True)
plt.show()