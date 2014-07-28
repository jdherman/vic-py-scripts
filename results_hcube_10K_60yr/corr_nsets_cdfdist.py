import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

data = np.transpose(np.loadtxt('vic_error_9p_10K.txt'))
ann10 = data[3]
ann10monR75 = data[5]

data = np.transpose(np.loadtxt('vic_hcube_param_cdfdist.txt'))
sumcd_ann10 = np.sum(data[2:], axis=0)

data = np.transpose(np.loadtxt('vic_hcube_param_cdfdist_r75.txt'))
sumcd_ann10monR75= np.sum(data[2:], axis=0)


print sumcd_ann10.size


plt.subplot(1,2,1)
plt.scatter(ann10,sumcd_ann10,linewidths=0)
plt.xlabel('Fraction Meeting Annual Error < 10%')
plt.ylabel('Sum of CDF Distances')
plt.title('For each grid cell ...')
plt.xlim([-0.1,1])
plt.ylim([0,4.5])


plt.subplot(1,2,2)
plt.scatter(ann10monR75,sumcd_ann10monR75,linewidths=0)
plt.xlabel('Fraction Meeting Annual Error < 10% && Monthly r > 0.75')
plt.ylabel('Sum of CDF Distances')
plt.title('For each grid cell ...')
plt.xlim([-0.1,1])
plt.ylim([0,4.5])


plt.show()





# m.pcolormesh(x,y,array_mask,vmin=0.0,vmax=10.0, cmap=ice, rasterized=True, edgecolor='0.6', linewidth=0)
# cbar = m.colorbar()
# cbar.solids.set_edgecolor("face")
# cbar.set_ticks([0,2,4,6,8,10])
# plt.title("VIC - Ann10monR75")
# plt.show()
