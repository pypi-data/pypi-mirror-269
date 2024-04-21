add function 

sejango - 3 arguments form(django),key(in form cleaned data),var(return if key is not find)


adder - dict,**kwargs 
add to dict all arguments kwargs



iswhiter(color(HEX),porog) - color=color for checking, porog = threshold for lightening
isdarker(color(HEX),porog) - color=color for checking, porog = threshold for darkering
brighness(rgb(RGB)) - rgb to float
hex_to_rgb(hex_xolor(HEX)) - you know


find(lst,sim) - lst=list sim=obj for searching, find obj inlist and return he index
 
listrand(min,max,kol): return random list


def IsKeyInDict(data, key): return bool: isvalid key in data



def stepen(number,stepan): degree of number
	
def faktorial(number): you know
	
def chibo(number): number of chibonachi
	
def summa(number):summ 
example:
    a=12
    print(summ(a))
this code return 3

class for django:


Color:
    abstract model
    for inheritance models add to model variable: color and function: isdarker, iswhite, hexrgb, rgbtofloat 


LBASE:
    
    add:
        context_paginator_name = name paginator for context
        page_n =  page-quantity for correct work need paginate_by
        page_n:
            if len(queryset)>=page_n:
                return (calculations for a given number of pages)
            else:
                return=paginate_by

    example:
    class index(LBASE):
        model=Tovar
        template_name="mains/icecream_list.html"
        context_object_name='date'
        paginate_by=5
        paginate_orphans=2
        page_n=5 ...