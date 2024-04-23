import javalang
import secrets
import random
import json
from nltk.corpus import wordnet
import os, random, re
import os, random
from shutil import copyfile
import ast
import wordninja
import re, random
from os import listdir
from os.path import isfile, join
from os import listdir
from os.path import isfile, join
class  CodeRefactor(object):
    def __init__(self): # real signature unknown
        pass
    def get_radom_var_name(self):
        res_string = ''
        for x in range(8):
            res_string += random.choice('abcdefghijklmnopqrstuvwxyz')
        return res_string


    def get_dead_for_condition(self):
        var = self.get_radom_var_name()
        return "int "+var+" = 0; "+var+" < 0; "+var+"++"


    def get_random_false_stmt(self):
        res = [random.choice(["True", "False"]) for x in range(10)]
        res.append("False")
        res_str = " and ".join(res)
        return res_str


    def get_tree(self,data):
        tokens = javalang.tokenizer.tokenize(data)
        parser = javalang.parser.Parser(tokens)
        tree = parser.parse_member_declaration()
        return tree



    def verify_method_syntax(self,data):
        try:
            tokens = javalang.tokenizer.tokenize(data)
            parser = javalang.parser.Parser(tokens)
            tree = parser.parse_member_declaration()
            print("syantax check passed")
        except:
            print("syantax check failed")


    def get_random_type_name_and_value_statment(self):
        datatype = random.choice(
            'byte,short,int,long,float,double,boolean,char,String'.split(','))
        var_name = self.get_radom_var_name()

        if datatype == "byte":
            var_value = self.get_random_int(-128, 127)
        elif datatype == "short":
            var_value = self.get_random_int(-10000, 10000)
        elif datatype == "boolean":
            var_value = random.choice(["True", "False"])
        elif datatype == "char":
            var_value = str(random.choice(
                'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')))
            var_value = '"'+var_value+'"'
        elif datatype == "String":
            var_value = str(self.get_radom_var_name())
            var_value = '"'+var_value+'"'
        else:
            var_value = self.get_random_int(-1000000000, 1000000000)

        mutant = str(var_name) + ' = ' + str(var_value)
        return mutant


    def generate_file_name_list_file_from_dir(self,method_path):
        filenames = [f for f in listdir(
            method_path) if isfile(join(method_path, f))]
        with open(method_path+'\\'+'all_file_names.txt', 'w') as f:
            f.write(json.dumps(filenames))
        print("done")


    def get_file_name_list(self,method_path):
        with open(method_path+'\\'+'all_file_names.txt') as f:
            data = json.load(f)
        return data


    def get_random_int(self,min, max):
        return random.randint(min, max)


    def format_code_chuncks(self,code_chuncks):
        for idx, c in enumerate(code_chuncks):
            c = c.replace(' . ', '.')
            c = c.replace(' ( ', '(')
            c = c.replace(' ) ', ')')
            c = c.replace(' ;', ';')
            c = c.replace('[ ]', '[]')
            code_chuncks[idx] = c
        return code_chuncks


    def format_code(self,c):
        c = c.replace(' . ', '.')
        c = c.replace(' ( ', '(')
        c = c.replace(' ) ', ')')
        c = c.replace(' ;', ';')
        c = c.replace('[ ]', '[]')
        return c


    def get_method_header(self,string):
        method_header = ''
        tree = self.get_tree(string)

        tokens = list(javalang.tokenizer.tokenize(string))

        chunck_start_poss = [s.position.column for s in tree.body]
        if len(chunck_start_poss) > 0:
            method_header = ' '.join([t.value for t in tokens
                                      if t.position.column < chunck_start_poss[0]])

        method_header = self.format_code_chuncks([method_header])[0]
        return method_header