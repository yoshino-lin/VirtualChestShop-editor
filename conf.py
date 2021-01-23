#按照times给string加缩进（空格）
def _addIndent(str_input:str,times:int,tab_space:int=2):
    for i in range(times*tab_space):
        str_input += " "
    return str_input

#处理string的模块
def _dictConverter(stringToWrite:str,dictToSave:dict,layer:int=0) -> str:
    for key in sorted(dictToSave):
        value = dictToSave[key]
        #如果值是列表
        if isinstance(value,dict):
            stringToWrite = _addIndent(
                _dictConverter(_addIndent(stringToWrite,layer)+key+" = {\n",value,layer+1)
                ,layer) + "}\n"
        #如果值是列表
        elif isinstance(value,list):
            stringToWrite = _addIndent(
                _listConverter(_addIndent(stringToWrite,layer)+key+" = [\n",value,layer+1),
                layer) + "]\n"
        #如果值是bool
        elif isinstance(value,bool):
            if value:
                stringToWrite = _addIndent(stringToWrite,layer) + '{0} = {1}\n'.format(key,"true")
            else:
                stringToWrite = _addIndent(stringToWrite,layer) + '{0} = {1}\n'.format(key,"false")
        #如果值是int
        elif isinstance(value,int):
            stringToWrite = _addIndent(stringToWrite,layer) + "{0} = {1}\n".format(key,value)
        #如果值是str
        elif isinstance(value,str):
            stringToWrite = _addIndent(stringToWrite,layer) + '{0} = "{1}"\n'.format(key,value)
        else:
            raise  Exception("Warning: Cannot recognize value {}'s data type!".format(value))
    return stringToWrite

def _listConverter(stringToWrite:str,listToSave:dict,layer:int) -> str:
    for value in listToSave:
        #如果值是字典
        if isinstance(value,dict):
            stringToWrite = _addIndent(
                _dictConverter(_addIndent(stringToWrite,layer) + "{\n",value,layer+1),
                layer) + "}\n"
        #如果值是列表
        elif isinstance(value,list):
            stringToWrite = _addIndent(
                _listConverter(_addIndent(stringToWrite,layer)+"[\n",value,layer+1),
                layer) + "]\n"
        #如果值是bool
        elif isinstance(value,bool):
            if value:
                stringToWrite = _addIndent(stringToWrite,layer)+'{}\n'.format("true")
            else:
                stringToWrite = _addIndent(stringToWrite,layer)+'{}\n'.format("false")
        #如果值是int
        elif isinstance(value,(int,str)):
            stringToWrite = _addIndent(stringToWrite,layer) + '"{}"\n'.format(value)
        else:
            raise  Exception("Warning: Cannot recognize value {}'s data type!".format(value))
    return stringToWrite

#保存文件
def dump(path:str,dictToSave:dict) -> None:
    with open(path,"w+",encoding='utf-8') as f: f.write(_dictConverter("",dictToSave))