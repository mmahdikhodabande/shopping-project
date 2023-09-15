def slider_list(custom_list, size):
    group_list = []
    for i in range(0, len(custom_list), size):
        group_list.append(custom_list[i:i + size])
    return group_list
