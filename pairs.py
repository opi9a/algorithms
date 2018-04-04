import numpy as np

# set global default target
glob_target = 10**9

def pair1(input_list, target=glob_target, _debug=False):

    pairs = []

    # go thru each member of list
    for i, num1 in enumerate(input_list):
        if _debug: print("Trying input list index ", i, ": ", num1)

    # test with each other number (i.e. rest of list)
        for j, num2 in enumerate(input_list[i+1:]):

            if _debug: print("  with ", num2)

            if num1 + num2 == target:
                if _debug:
                    print("FOUND PAIR: {}({}) + {}({}) = {}".format(num1,
                                                            i, num2, j+i+1, num1 + num2))
                pairs.append(max(num1, target-num1))
                break

    return pairs


def pair1a(input_list, target=glob_target, _debug=False):
    # sort list
    # take first member
    # add to last member, test
    # repeat as long as sums are > target

    pairs = []

    input_list = np.sort(input_list)

    # go thru each member of list
    for i, num1 in enumerate(input_list):
        if _debug: print("Trying input list index ", i, ": ", num1)

    # start from end and compare until sum is < target
    # test with each other number (i.e. rest of list)
        temp_sum = target + 1
        ind = len(input_list) - 1

        while temp_sum >= target and ind > i:

            num2 = input_list[ind]
            temp_sum = num1 + num2

            if temp_sum == target:
                if _debug:
                    print("FOUND PAIR: {}({}) + {}({}) = {}".format(num1,
                                                            i, num2, ind, temp_sum))
                pairs.append(max(num1, target-num1))
                break

            if _debug:
                print("temp sum is", temp_sum)
                print("index ind is", ind)

            ind -= 1

    return pairs



def pair2(input_list, target=glob_target, _debug=False):

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
            if _debug:
                print("FOUND PAIR: {}({}) + {}({}) = {}"
                        .format(complement, log[complement], num, i, num + complement))

            # add to results
            pairs.append(max(num, target-num))

        log[num] = i

    return pairs


def make_test_list(scope, size=None, size_ratio=0.1):

    if size == None:
        size = int(scope*size_ratio)

    return np.random.randint(0, high=scope, size=size)




