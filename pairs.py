import numpy as np

def pair1(input_list, target=None, _debug=False):

	if target is None:
		target = int(len(input_list)*0.1)

	pairs = []

	# go thru each member of list
	for i, num1 in enumerate(input_list):
		if _debug: print("Trying input list index ", i, ": ", num1)

	# test with each other number (i.e. rest of list)
		for j, num2 in enumerate(input_list[i+1:]):

			if _debug: print("  with ", num2)

			if num1 + num2 == target:
				print("FOUND PAIR: {}({}) + {}({}) = {}".format(num1, i, num2, j+i+1,
																	 num1 + num2))
				pairs.append((log[complement], i))
				break

	return pairs


def pair2(input_list, target=None, _debug=False):

	if target is None:
		target = int(len(input_list)*0.1)
	
	log = {}
	pairs = []

	# go thru each member of list
	for i, num in enumerate(input_list):
		if _debug: 
			print("Trying input list index ", i, ": ", num)
			print("log: ", [x for x in log.keys()])	
	
		# make complement and check if already seen
		complement = target - num
	

		if log.get(complement, False):
			print("FOUND PAIR: {}({}) + {}({}) = {}"
						.format(complement, log[complement], num, i, num + complement))

			# add to results
			pairs.append((log[complement], i))

		log[num] = i

	return pairs


def make_test_list(scope, size=None, size_ratio=0.1):

	if size == None:
		size = int(scope*size_ratio)

	return np.random.randint(0, high=scope, size=size)
