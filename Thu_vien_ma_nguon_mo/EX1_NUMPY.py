import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([[1 ,2 ,3],[4, 5, 6]])

result1 = arr1[:3] + arr2 
result2 = arr1 * 2
result3 = np.mean(arr2, axis = 1)

element = arr1[2]
subarray = arr2[:,1]

arr3 = arr1.reshape(5,1)
sorted_arr = np.sort(arr2, axis = 0)

sin_values = np.sin(arr1)
dot_product = np.dot(arr1[:2], arr2)

print(arr1)
print(result2)
print(result3)
print(element)
print(subarray)
print(arr3)
print(sorted_arr)
print(sin_values)
print(dot_product)