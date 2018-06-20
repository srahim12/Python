# Programmed By: 	Shah Rahim
# Course:			Intro to Data Science
# Semester:			Spring 2018
# Assignment:		Vector Representations


# NOTE--> Please go down to the main() function on the bottom of this code


import numpy as np

text_file = 'glove.6B.300d.txt'

def cos_sim(name_vector, target_vector):
	dot_product = np.dot(name_vector, target_vector)
	norm_name = np.linalg.norm(name_vector)
	norm_target = np.linalg.norm(target_vector)
	return dot_product / (norm_name * norm_target)

def getFloat(lis):
	float_lis = [float(i) for i in lis]
	return float_lis

def getTopFive(lis):
	return [lis[i] for i in np.argsort(lis)[-5:]]

def removeFromDict(dic,five_neighbors):
	for i in dic:
		if(i not in five_neighbors):
			del dic[i]
			break
	return dic

def getIndex(words,target):
	target_index = 0
	for i in words:
		if(target in i.split()):
			break
		target_index+=1
	return target_index

def componentSum(avg_vec,word_vec):
	for i in range(0,len(avg_vec)):
		avg_vec[i] = avg_vec[i] + word_vec[i]
	return avg_vec

def componentDiv(sum_vec,size):
	for i in range(0,len(sum_vec)):
		sum_vec[i] = sum_vec[i] / size
	return sum_vec

def getNeighbors(i,main_vector,five_neighbors,dic):
		lis = []
		target_list = i.split()[1:]
		target_vector = getFloat(target_list)
		cos = cos_sim(main_vector,target_vector)
		five_neighbors.append(cos)
		dic[cos] = i.split()[0]
		if(len(five_neighbors) >5):
			five_neighbors = getTopFive(five_neighbors)
			dic = removeFromDict(dic,five_neighbors)
		lis.append(five_neighbors)
		lis.append(dic)
		return lis

def vecRep(words,s):
	s_list = s.split()
	s_dict = {}
	exists = 0
	for i in words:
		if(i.split()[0] in s_list):
			s_dict[i.split()[0]] = getFloat(i.split()[1:])
			exists+=1
			if(exists>=len(s_list)):
				break
	avg_vec = [0]*300
	for key in s_dict.keys():
		avg_vec = componentSum(avg_vec,s_dict[key])
	avg_vec = componentDiv(avg_vec, len(s_list))
	return avg_vec



def task1():
	with open(text_file, 'r', encoding="utf8") as f:
	    words = list(f)
	name = 'leonardo'
	array = []
	print('Running task_1 please give it a couple minutes...')
	print('First name is Shah and it does not exists in the data.... Using: ' + name+'\n')
	name_index = getIndex(words,name)
	first_name = words[name_index].split()[1:]
	name_vector = getFloat(first_name)
	dic = {}
	index = 0
	five_neighbors = []
	for i in words:
		if(index !=name_index):
			lis = getNeighbors(i,name_vector,five_neighbors,dic)
			five_neighbors = lis[0]
			dic = lis[1]
		index +=1
	for i in dic:
		print(dic[i] + ' has a score of: ' + str(i))

def task2():
	with open(text_file, 'r', encoding="utf8") as f:
	    words = list(f)
	print('Running task_2 please give it a couple minutes...')
	s_0 = 'tell me your name please'
	s0_lis = s_0.split()
	s0_index_lis = [0]*len(s0_lis)
	s0_index = 0
	for i in s0_lis:
		s0_index_lis[s0_index] = getIndex(words,s0_lis[s0_index])
		s0_index+=1

	s0_vec_rep = vecRep(words,s_0)
	five_neighbors = []
	dic = {}
	index = 0
	for i in words:
		if(index not in s0_index_lis):
			lis = getNeighbors(i,s0_vec_rep,five_neighbors,dic)
			five_neighbors = lis[0]
			dic = lis[1]
		index +=1

	for i in dic:
		print(dic[i] + ' has a score of: ' + str(i))

def task3():
	with open(text_file, 'r', encoding="utf8") as f:
	    words = list(f)
	
	s_0 = 'tell me your name please'
	s_1 = 'may i know your label'
	s_2 = 'chocolate ice cream fudge brownie'

	s0_vec_rep = vecRep(words,s_0)
	s1_vec_rep = vecRep(words,s_1)
	s2_vec_rep = vecRep(words,s_2)
	
	s0_s1_cos_sim = cos_sim(s0_vec_rep,s1_vec_rep)
	s0_s2_cos_sim = cos_sim(s0_vec_rep,s2_vec_rep)

	print('Cos-Similarity for s_0 and s_1 is: ' + str(s0_s1_cos_sim))
	print('\n')
	print('Cos-Similarity for s_0 and s_2 is: ' + str(s0_s2_cos_sim))
	print('\n')
	print('The obtained cosine similarity score for s_0 and s_1 is reasonable with 0.866. Although the words are different, the meaning is similar so the score is quite good')
	print('The obtained cosine similarity score for s_0 and s_2 is reasonable with 0.192. The meanings are disimilar so therefore the score reflects this')

	

# Please de-comment the functions corresponding to the tasks and run the program
# For Cosine Similarity and Vector Representation, I wrote separate functions and incorporated them into my tasks for cleaner code. I also wrote helper functions for the same purppose

#task1()
#task2()
#task3()
