import re,collections
from ShowPie import show_pie
def get_words(file):  
	with open (file) as f:  
		words_box=[]  
		for line in f:                           
			if re.match(r'[a-zA-Z0-9]*',line):#避免中文影响  
				words_box.extend(line.strip().split())                 
	return dict(collections.Counter(words_box))

words_sum = 0
words_dict = get_words('./color.log')
 

print(words_dict)

for i in words_dict:
	words_sum += words_dict[i]

print('Sum: ' + str(words_sum))

word_percent = lambda x:round(x / words_sum * 100, 3)

words_percent_dict = {}
for i in words_dict:
	words_percent_dict[i] = word_percent(words_dict[i])

print(words_percent_dict)
show_pie(words_percent_dict)