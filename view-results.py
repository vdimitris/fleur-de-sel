from matplotlib import pyplot
import numpy

numpy.set_printoptions(suppress=True)
plot_results = numpy.loadtxt("results/scenario_1000000_15_1_7_1-rounds-100.txt")

print(plot_results)

means = numpy.mean(plot_results, axis = 0)

print("user time mean:", f'{means[1]:.7f}')
print("attacker time mean:", f'{means[2]:.7f}')

pyplot.plot(plot_results[:,0], plot_results[:,1], marker="o", color = "blue", label = "system")
pyplot.plot(plot_results[:,0], plot_results[:,2], marker="o", color = "red", label = "attacker")   
pyplot.xlabel("# try")
pyplot.ylabel("duration (sec)")
pyplot.legend()
pyplot.show()
