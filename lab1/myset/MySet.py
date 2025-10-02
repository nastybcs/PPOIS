class Set:
    def __init__(self, input_str):
        self.elements=self._parse_string(input_str)
   
    def _nesting_check(self, depth, i, input_str, temp_element):
        if input_str[i]=='{':
            depth[0]+=1
            i+=1
            while not (input_str[i]=='}' and depth[0]<=2):
                if input_str[i]=='{':
                    depth[0]+=1
                elif input_str[i]=='}':
                    depth[0]-=1
                temp_element.append(input_str[i]) 
                i+=1
            depth[0]-=1
        else:
            temp_element.append(input_str[i])
        return i 
    
    def _parse_string(self, input_str):
        input_str=input_str.replace(" ","") 
        cleaned=[]
        for i, ch in enumerate(input_str):
            if i>0 and ((ch==',' and input_str[i-1]==',') or (ch ==',' and input_str[i-1]=='{')):
                continue
            cleaned.append(ch)
        input_str="".join(cleaned)

        result=[]
        temp_element=[]
        depth=[1]
        i=1
        while(i<len(input_str)):
            if(input_str[i]=="," or (input_str[i]=='}' and depth[0]==1)):
                result.append(["".join(temp_element)])
                temp_element =[]
                i+=1
                continue
            i=self._nesting_check(depth,i, input_str,temp_element)
            i+=1
        if temp_element != []:  
            result.append(["".join(temp_element)])
        return result
    
    
    def print_set(self):
        print("{", end="")  
        for i, element in enumerate(self.elements):
            print("{", end="") 
       
            print("".join(element), end="")
            print("}", end="")  
            if i < len(self.elements) - 1:
                print(",", end="")
        print("}")  

    def add_element(self,new_element):
        elems_to_add=self._parse_string(new_element)
        for el in elems_to_add:
            if el=="{}" and el not in self.elements:
                self.elements.append("")
            elif el not in self.elements:
                self.elements.append(el)
    def remove_element(self, target_element):
        elem_to_del=self._parse_string(target_element)
        new_elements=[]
        for el in self.elements:
            if el not in elem_to_del:
                new_elements.append(el)
        self.elements=new_elements
    def cantorovo_algorithm(self,elements):
        if len(elements) <=2:
            return elements
        count = len(elements)//3
        left_third =elements[:count]
        right_third = elements[-count:]

        left_result =self.cantorovo_algorithm(left_third)
        right_result = self.cantorovo_algorithm(right_third)
        return left_result+right_result
    
    def get_size(self):
        return len(self.elements)
    
    def __getitem__(self,item):
        if item == "{}":
            item_list=[""]
        else:
            item_list=self._parse_string(item)[0]
        for el in self.elements:
            if el== item_list:
                return True
        return False
    def __add__(self, other):
        new_set=Set("{}")
        new_set.elements=[el for el in self.elements]

        for el in other.elements:
            if el not in self.elements:
                new_set.elements.append(el)
        return new_set
    def __iadd__(self, other):
       
        for el in other.elements:
            if el not in self.elements:
                self.elements.append(el)
        return self
    
    def __mul__(self, other):
        new_set = Set("{}")
        new_set.elements = [el for el in self.elements if el in other.elements and el != [""]]
        return new_set

    def __imul__(self, other):
        self.elements = [el for el in self.elements if el in other.elements]
        return self


    def __sub__(self, other):
        new_set = Set("{}")
        new_set.elements = [el for el in self.elements if el not in other.elements]
        return new_set

    def __isub__(self, other):
        self.elements = [el for el in self.elements if el not in other.elements]
        return self
    def boolean(self):
        result=[[]]

        for el in self.elements:
            new_subsets=[]
            for subset in result:
                new_subsets.append(subset+[el])
            result.extend(new_subsets)
        print(f"Булеан множества (всего {len(result)} подмножеств):")
        for subset in result:
            print("{", end="")
            for elem in subset:
                print("{", end="")
                print("".join(elem), end="")
                print("}", end="")
            print("}")
   

