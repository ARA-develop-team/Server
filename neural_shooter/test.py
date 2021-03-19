import matplotlib.pyplot as plt

y = [[574], [565.875], [609], [605], [606], [606], [612], [613], [610], [603], [607], [600], [589], [585], [586], [591],
     [592], [591], [543], [448], [588], [591], [597], [599], [524]]

array = [[1, 2], [3, 5]]
for x in array:
    print(x)

# plt.plot(y, label='line', color='blue')
# plt.plot(midline, label='line', color='red')
plt.title('MAIN')
plt.xlabel('seconds')
plt.ylabel('cycle')
plt.grid(True)
plt.show()
