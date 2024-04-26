def get_list_intersection(list_of_lists):
    intersection_list=[]
    for index,List in enumerate(list_of_lists):
        if index==0:
            intersection_list=list(set(list_of_lists[index]).intersection(set(list_of_lists[index+1])))

        else:
            intersection_list=list(set(intersection_list).intersection(set(List)))
    return intersection_list


