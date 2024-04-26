def alldel(target,delarray):
    counter = []
    for i,li in enumerate(target):
        pol = True
        for li2 in delarray:
            if i == li2:
                pol =False
                break
        if pol ==True:
            counter.append(li)
    return counter
