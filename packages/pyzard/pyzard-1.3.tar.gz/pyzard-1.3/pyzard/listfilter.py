import pyzard

def listfilter(mod,filter,list):
    """
    mod -> True
        키워드가 들어있는 인자만 도출
    mod -> False
        키워드가 없는 인자만 도출
    ※각 인자 모드 리스트입니다.※
    """
    if mod == False:
        prereturn_lst = []
        for li in filter:
            for li2 in list:
                if not li in li2:
                    continue
                prereturn_lst.append(li2)
        return_lst = pyzard.sublist(list,prereturn_lst)

    if mod == True:
        prereturn_lst = []

        for li in filter:
            for li2 in list:
                if li in li2:
                    prereturn_lst.append(li2)
                
        return_lst = pyzard.deloverlap(prereturn_lst)
    return return_lst

