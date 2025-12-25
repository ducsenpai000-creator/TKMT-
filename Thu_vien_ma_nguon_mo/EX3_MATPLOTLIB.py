import matplotlib.pyplot as plt
import numpy as np 

x = np.linspace(0, 2 *np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (10,8))

axes[0, 0].plot (x, y1)
axes[0, 0].set_title('đồ thị sin')

axes[0, 1].scatter(x, y2)
axes[0, 1].set_title('đồ thị phân tán')

axes[1, 0].bar(np.arange(5),np.random.rand(5))
axes[1, 0].set_title('Bieu do cot')

axes[1, 1].imshow(np.random.rand(10,10), cmap = 'hot')
axes[1, 1].set_title('bieu do nhiet do')

plt.tight_layout()
plt.show()
