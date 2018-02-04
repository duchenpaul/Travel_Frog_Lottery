import matplotlib.pyplot as plt

def show_pie(dict):
	# Data to plot
	labels = [ i for i in dict]
	sizes = [ dict[i] for i in dict]
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	colors = [ i.lower().replace('!', '') for i in dict]
	explode = (0, 0, 0, 0)  # explode 1st slice

	# Plot
	plt.pie(sizes, labels=labels, colors=colors,#explode=explode, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=140)

	plt.axis('equal')
	plt.show()

if __name__ == '__main__':
	labelsz = ['Python', 'C++', 'Ruby', 'Java']
	sizesz = [215, 130, 2445, 210]
	dict = {}
	for i, label in enumerate(labelsz):
		dict[label] = sizesz[i]

	show_pie(dict)