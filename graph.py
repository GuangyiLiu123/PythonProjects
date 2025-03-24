import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 1000)  # Time range

# Define x and y components
x = 3 * np.cos(t) + 1 * np.sin(t)
y = np.cos(t) + np.sin(t)

plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Phase Portrait")
plt.axis("equal")  # Keep aspect ratio
plt.grid()
plt.show()
