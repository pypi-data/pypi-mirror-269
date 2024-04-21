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


    def get_method_statement(self,string):
        code_chuncks = []
        tree = self.get_tree(string)
        tokens = list(javalang.tokenizer.tokenize(string))
        chunck_start_poss = [s.position.column for s in tree.body]

        if len(chunck_start_poss) > 1:
            for idx, statement in enumerate(chunck_start_poss[:-1]):
                statment = ' '.join([t.value for t in tokens
                                     if t.position.column >= chunck_start_poss[idx]
                                     and t.position.column < chunck_start_poss[idx+1]])
                code_chuncks.append(statment)

            last_statment = ' '.join([t.value for t in tokens
                                      if t.position.column >= chunck_start_poss[-1]][:-1])
            code_chuncks.append(last_statment)

        if len(chunck_start_poss) == 1:
            last_statment = ' '.join([t.value for t in tokens
                                      if t.position.column >= chunck_start_poss[0]][:-1])
            code_chuncks.append(last_statment)
        code_chuncks = self.format_code_chuncks(code_chuncks)
        return code_chuncks


    def scan_tree(self,tree):
        for path, node in tree:
            print("=======================")
            print(node)


    def get_all_type(self,tree):
        res_list=[]
        for path, node in tree.filter(javalang.tree.ReferenceType):
            if node.name != None:
                res_list.append(node.name)
        return list(set(res_list))


    def scan_local_vars(self,tree):
        for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
            print("name=========type=============")
            print(node.declarators[0].name, "\t", node.type.name)


    def get_local_vars(self,tree):
        var_list = []
        for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
            var_list.append([node.declarators[0].name, node.type.name])
        return var_list


    def get_local_assignments(self,tree):
        var_list = []
        for path, node in tree.filter(javalang.tree.Assignment):
            var_list.append([node.declarators[0].name, node.type.name])
        return var_list


    def get_branch_if_else_mutant(self):
        mutant = self.get_random_type_name_and_value_statment() + ' if '+self.get_random_false_stmt() + ' else ' + str(self.get_random_int(-1000000000, 1000000000))
        return mutant


    def get_branch_if_mutant(self):
        mutant = 'if '+self.get_random_false_stmt()+': ' + \
            self.get_random_type_name_and_value_statment()
        return mutant


    def get_branch_while_mutant(self):
        mutant = 'while '+self.get_random_false_stmt()+': ' + \
            self.get_random_type_name_and_value_statment()
        return mutant


    def get_branch_for_mutant(self):
        var = self.get_radom_var_name()
        mutant = 'for ' + var + ' in range(0): ' + self.get_random_type_name_and_value_statment()
        return mutant

    def word_synonym_replacement(self,word):
        if len(word) <= 3:
            return word + '_new'
        word_set = wordninja.split(word)
        while True:
            if word_set == []:
                return word + '_new'
            word_tar = random.choice(word_set)
            word_syn = wordnet.synsets(word_tar)
            if word_syn == []:
                word_set.remove(word_tar)
            else:
                break
        word_ret = []
        for syn in word_syn:
            word_ret = word_ret + syn.lemma_names()
            if word_tar in word_ret:
                word_ret.remove(word_tar)
        try:
            self.word_new = random.choice(word_ret)
        except:
            self.word_new = word

        return word.replace(word_tar, self.word_new), word_ret


    def extract_method_name(self,string):
        match_ret = re.search('\w+\s*\(',string)
        if match_ret:
            method_name = match_ret.group()[:-1].strip()
            return method_name
        else:
            return None


    def extract_argument(self,string):
        end_pos    = string.find(')')
        sta_pas    = string.find('(')
        arguments  = string[sta_pas + 1: end_pos + 1].strip()[:-1]
        arguments_list = arguments.split(',')
        if ' ' in arguments_list:
            arguments_list.remove(' ')
        if '' in arguments_list:
            arguments_list.remove('')
        return arguments_list


    def extract_brace_python(self,string, start_pos):
        fragment = string[start_pos:]
        line_list = fragment.split('\n')
        return_string = ''
        return_string += line_list[0] + '\n'
        space_min = 0
        for _ in range(1, len(line_list)):
            space_count = 0
            for char in line_list[_]:
                if char == ' ':
                    space_count += 1
                else:
                    break
            if _ == 1:
                space_min = space_count
                return_string += line_list[_] + '\n'
            elif space_count < space_min and space_count != len(line_list[_]):
                break
            else:
                return_string += line_list[_] + '\n'
        return_string = return_string[:-1]
        return return_string


    def extract_class(self,string):

        class_list = []
        while ' class ' in string:
            start_pos  = string.find(' class ')
            class_text = self.extract_brace_python(string, start_pos)
            class_list.append(class_text)
            string = string.replace(class_text, '')

        while 'class ' in string:
            start_pos  = string.find('class ')
            class_text = self.extract_brace_python(string, start_pos)
            class_list.append(class_text)
            string = string.replace(class_text, '')

        return class_list, string


    def extract_function_python(self,string):
        i = 0
        function_list = []
        # print(string)
        while True:
            match_ret = re.search('(def).+\s*\(', string)
            # print(match_ret)
            if match_ret:
                function_head = match_ret.group()
                start_pos = string.find(function_head)
                function_text = self.extract_brace_python(string, start_pos)
                function_list.append(function_text)
                string = string.replace(function_text, 'vesal'+ str(i))
                i+=1
            else:
                break
        return function_list, string


    def extract_for_loop(self,string):

        for_list = []
        while True:
            # match_ret = re.search('for\s+\(', string)
            match_ret = re.search(' for ', string)
            if match_ret:
                for_head = match_ret.group()
                start_pos = string.find(for_head)
                for_text = self.extract_brace_python(string, start_pos)
                for_list.append(for_text)
                string = string.replace(for_text, '')
            else:
                break
        return for_list


    def extract_if(self,string):

        if_list = []
        while True:
            match_ret = re.search(' if ', string)
            if match_ret:
                if_head = match_ret.group()
                start_pos = string.find(if_head)
                if_text = self.extract_brace_python(string, start_pos)
                if_list.append(if_text)
                string = string.replace(if_text, '')
            else:
                break
        return if_list


    def extract_while_loop(self,string):

        while_list = []
        while True:
            match_ret = re.search(' while ', string)
            if match_ret:
                while_head = match_ret.group()
                start_pos = string.find(while_head)
                while_text = self.extract_brace_python(string, start_pos)
                while_list.append(while_text)
                string = string.replace(while_text, '')
            else:
                break
        return while_list, string


    def hack(self,source):
        root = ast.parse(source)

        for node in ast.walk(root):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                yield node.id
            elif isinstance(node, ast.Attribute):
                yield node.attr
            elif isinstance(node, ast.FunctionDef):
                yield node.name


    def extract_local_variable(self,string):
        return list(self.hack(string))

    def rename_local_variable(self,method_string):
        local_var_list = self.extract_local_variable(method_string)
        if len(local_var_list) == 0:
            return method_string

        mutation_index = random.randint(0, len(local_var_list) - 1)
        return method_string.replace(local_var_list[mutation_index], self.word_synonym_replacement(local_var_list[mutation_index])[0])


    def add_local_variable(self,method_string):
        local_var_list = self.extract_local_variable(method_string)
        if len(local_var_list) == 0:
            return method_string

        mutation_index = random.randint(0, len(local_var_list) - 1)
        match_ret = re.search(local_var_list[mutation_index] + '=\w', method_string)
        if match_ret is None:
            match_ret = re.search(local_var_list[mutation_index] + ' = ', method_string)
        if match_ret is None:
            match_ret = re.search(local_var_list[mutation_index] + '= ', method_string)
        if match_ret:
            var_definition      = match_ret.group()[:-1]
            new_var_definition  = var_definition.replace(local_var_list[mutation_index], self.word_synonym_replacement(local_var_list[mutation_index])[0])
            method_string       = method_string.replace(var_definition, var_definition + '' + new_var_definition)
            return method_string
        else:
            return method_string


    def duplication(self,method_string):
        local_var_list = self.extract_local_variable(method_string)
        if len(local_var_list) == 0:
            return method_string
        mutation_index = random.randint(0, len(local_var_list) - 1)
        match_ret = re.search(local_var_list[mutation_index] + '=\w', method_string)
        if match_ret is None:
            match_ret = re.search(local_var_list[mutation_index] + ' = ', method_string)
        if match_ret is None:
            match_ret = re.search(local_var_list[mutation_index] + '= ', method_string)
        if match_ret:
            var_definition = match_ret.group()[:-1]
            new_var_definition = var_definition
            method_string = method_string.replace(var_definition, var_definition + new_var_definition)
            # print(method_string)
            return method_string
        else:
            # print(method_string)
            return method_string


    def rename_api(self,method_string):
        match_ret      = re.findall(' \s*\w+\s*\(', method_string)
        match_ret = match_ret[1:]
        if match_ret != []:
            api_name = random.choice(match_ret)[1:-1]
            return method_string.replace(api_name, self.word_synonym_replacement(api_name)[0])
        else:
            return method_string


    def rename_method_name(self,method_string):
        method_name = self.extract_method_name(method_string)
        if method_name:
            return method_string.replace(method_name, self.word_synonym_replacement(method_name)[0])
        else:
            return method_string


    def rename_argument(self,method_string):
        arguments_list = self.extract_argument(method_string)
        if len(arguments_list) == 0:
            return method_string

        mutation_index = random.randint(0, len(arguments_list) - 1)
        return method_string.replace(arguments_list[mutation_index], self.word_synonym_replacement(arguments_list[mutation_index]))


    def return_optimal(self,method_string):
        if 'return ' in method_string:
            return_statement  = method_string[method_string.find('return ') : method_string.find('\n', method_string.find('return ') + 1)]
            return_object     = return_statement.replace('return ', '')
            if return_object == 'null':
                return method_string
            optimal_statement = 'return 0 if (' + return_object + ' == None) else ' + return_object
            method_string = method_string.replace(return_statement, optimal_statement)
        return method_string


    def enhance_for_loop(self,method_string):
        for_loop_list = self.extract_for_loop(method_string)
        if for_loop_list == []:
            return method_string

        mutation_index = random.randint(0, len(for_loop_list) - 1)
        for_text = for_loop_list[mutation_index]
        for_info = for_text[for_text.find('(') + 1 : for_text.find(')')]
        if ' range(' in for_text:
            if ',' not in for_info:
                new_for_info = '0, ' + for_info
                method_string = method_string.replace(for_info, new_for_info)
            elif len(for_info.split(',')) == 2:
                new_for_info = for_info + ' ,1'
                method_string = method_string.replace(for_info, new_for_info)
            else:
                new_for_info = for_info + '+0'
                method_string = method_string.replace(for_info, new_for_info)
            return method_string

        else:
            return method_string


    def add_print(self,method_string):
        statement_list = method_string.split('\n')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement      = statement_list[mutation_index]
        if statement == '':
            return method_string
        space_count = 0
        if mutation_index == len(statement_list) - 1:
            refer_line = statement_list[-1]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        else:
            refer_line = statement_list[mutation_index]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        new_statement = ''
        for _ in range(space_count):
            new_statement += ' '
        new_statement += 'print("' + str(random.choice(self.word_synonym_replacement(statement)[1])) + '")'
        method_string = method_string.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def enhance_if(self,method_string):
        if_list = self.extract_if(method_string)
        mutation_index = random.randint(0, len(if_list) - 1)
        if_text = if_list[mutation_index]
        if_info = if_text[if_text.find('if ') + 3: if_text.find(':')]
        new_if_info = if_info
        if 'true' in if_info:
            new_if_info = if_info.replace('true', ' (0==0) ')
        if 'flase' in if_info:
            new_if_info = if_info.replace('flase', ' (1==0) ')
        if '!=' in if_info and '(' not in if_info and 'and' not in if_info and 'or' not in if_info:
            new_if_info = if_info.replace('!=', ' is not ')
        if '<' in if_info and '<=' not in if_info and '(' not in if_info and 'and' not in if_info and 'or' not in if_info:
            new_if_info = if_info.split('<')[1] + ' > ' + if_info.split('<')[0]
        if '>' in if_info and '>=' not in if_info and '(' not in if_info and 'and' not in if_info and 'or' not in if_info:
            new_if_info = if_info.split('>')[1] + ' < ' + if_info.split('>')[0]
        if '<=' in if_info and '(' not in if_info and 'and' not in if_info and 'or' not in if_info:
            new_if_info = if_info.split('<=')[1] + ' >= ' + if_info.split('<=')[0]
        if '>=' in if_info and '(' not in if_info and 'and' not in if_info and 'or' not in if_info:
            new_if_info = if_info.split('>=')[1] + ' <= ' + if_info.split('>=')[0]
        if '==' in if_info:
            new_if_info = if_info.replace('==', ' is ')

        return method_string.replace(if_info, new_if_info)


    def add_argumemts(self,method_string):
        arguments_list = self.extract_argument(method_string)
        arguments_info = method_string[method_string.find('(') + 1: method_string.find(')')]
        if len(arguments_list) == 0:
            arguments_info = self.word_synonym_replacement(self.extract_method_name(method_string))[0]
            return method_string[0 : method_string.find('()') + 1] + arguments_info + method_string[method_string.find('()') + 1 :]
        mutation_index = random.randint(0, len(arguments_list) - 1)
        org_argument = arguments_list[mutation_index]
        new_argument = self.word_synonym_replacement(arguments_list[mutation_index])
        new_arguments_info = arguments_info.replace(org_argument, org_argument + ', ' + new_argument)
        method_string = method_string.replace(arguments_info, new_arguments_info, 1)
        return method_string


    def enhance_filed(self,method_string):
        arguments_list = self.extract_argument(method_string)
        line_list = method_string.split('\n')
        refer_line = line_list[1]
        if len(arguments_list) == 0:
            return method_string
        space_count = 0
        for char in refer_line:
            if char == ' ':
                space_count += 1
            else:
                break
        mutation_index = random.randint(0, len(arguments_list) - 1)
        space_str = ''
        for _ in range(space_count):
            space_str += ' '
        extra_info = "\n" + space_str + "if " + arguments_list[mutation_index].strip().split(' ')[-1] + " == None: print('please check your input')"
        method_string = method_string[0 : method_string.find(':') + 1] + extra_info + method_string[method_string.find(':') + 1 : ]
        return method_string


    def apply_plus_zero_math(self,data):
        variable_list = self.extract_local_variable(data)
        success_flag = 0
        for variable_name in variable_list:
            match_ret = re.findall(variable_name + '\s*=\s\w*\n', data)
            if len(match_ret) > 0:
                code_line = match_ret[0]
                value = code_line.split('\n')[0].split('=')[1]
                ori_value = value
                if '+' in value or '-' in value or '*' in value or '/' in value or '//' in value:
                    value = value + ' + 0'
                    success_flag = 1
                try:
                    value_float = float(value)
                    value = value + ' + 0'
                    success_flag = 1
                except ValueError:
                    continue
                if success_flag == 1:
                    mutant = code_line.split(ori_value)[0]
                    mutant = mutant + value + '\n'
                    method_string = data.replace(code_line, mutant)
                    return method_string
        if success_flag == 0:
            return data


    def dead_branch_if_else(self,data):
        statement_list = data.split('\n')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        space_count = 0
        if statement == '':
            return data
        if mutation_index == len(statement_list) - 1:
            refer_line = statement_list[-1]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        else:
            refer_line = statement_list[mutation_index]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        new_statement = ''
        for _ in range(space_count):
            new_statement += ' '
        new_statement += self.get_branch_if_else_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def dead_branch_if(self,data):
        statement_list = data.split('\n')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        space_count = 0
        if statement == '':
            return data
        if mutation_index == len(statement_list) - 1:
            refer_line = statement_list[-1]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        else:
            refer_line = statement_list[mutation_index]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        new_statement = ''
        for _ in range(space_count):
            new_statement += ' '
        new_statement += self.get_branch_if_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)

        return method_string


    def dead_branch_while(self,data):
        statement_list = data.split('\n')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        space_count = 0
        if statement == '':
            return data
        if mutation_index == len(statement_list) - 1:
            refer_line = statement_list[-1]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        else:
            refer_line = statement_list[mutation_index]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        new_statement = ''
        print(space_count)
        for _ in range(space_count):
            new_statement += ' '
        new_statement += self.get_branch_while_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        # print(method_string)
        return method_string


    def dead_branch_for(self,data):
        statement_list = data.split('\n')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        space_count = 0
        if statement == '':
            return data
        if mutation_index == len(statement_list) - 1:
            refer_line = statement_list[-1]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        else:
            refer_line = statement_list[mutation_index]
            for char in refer_line:
                if char == ' ':
                    space_count += 1
                else:
                    break
        new_statement = ''
        for _ in range(space_count):
            new_statement += ' '
        new_statement += self.get_branch_for_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string

    def return_function_code(self,code, method_names):
        final_codes = []
        final_names = []
        Class_list, raw_code = self.extract_class(code)
        for class_name in Class_list:
            function_list, class_name = self.extract_function_python(class_name)
        for fun_code in function_list:
            for method_name in method_names:
                method_name_tem = method_name.replace('|', '')
                if method_name_tem.upper() in fun_code.split('\n')[0].upper():

                    final_codes.append(fun_code)
                    final_names.append(method_name)
        return final_codes, final_names


    def generate_adversarial(self,k, code, method_names):
            method_name = method_names[0]
            function_list = []
            class_name = ''
            Class_list, raw_code = self.extract_class(code)
            for class_name in Class_list:
                function_list, class_name = self.extract_function_python(class_name)

            refac = []
            new_refactored_code = ''
            for code in function_list:
                if method_name not in code.split('\n')[0]:
                    continue
                new_rf = code
                new_refactored_code = code
                for t in range(k):
                    refactors_list = [self.rename_argument,
                                      self.return_optimal,
                                      self.add_argumemts,
                                      self.rename_api,
                                      self.rename_local_variable,
                                      self.add_local_variable,
                                      self.rename_method_name,
                                      self.enhance_if,
                                      self.add_print,
                                      self.duplication,
                                      self.apply_plus_zero_math,
                                      self.dead_branch_if_else,
                                      self.dead_branch_if,
                                      self.dead_branch_while,
                                      self.dead_branch_for,
                                      # dead_branch_switch
                                      ]#
                    vv = 0
                    while new_rf == new_refactored_code and vv <= 20:
                        try:
                            vv += 1
                            refactor       = random.choice(refactors_list)
                            print('*'*50 , refactor , '*'*50)
                            new_refactored_code = refactor(new_refactored_code)

                        except Exception as error:
                            print('error:\t', error)

                    new_rf = new_refactored_code
                    print('----------------------------OUT of WHILE----------------------------------', vv)
                    print('----------------------------CHANGED THJIS TIME:----------------------------------', vv)
                refac.append(new_refactored_code)
            code_body = raw_code.strip() + ' ' + class_name.strip()
            for i in range(len(refac)):
                final_refactor = code_body.replace('vesal' + str(i), str(refac[i]))
                code_body = final_refactor
            return new_refactored_code


    def generate_adversarial_json(self,k, code):
        final_refactor = ''
        function_list = []
        class_name = ''
        vv = 0
        if len(function_list) == 0:
            function_list.append(code)
        refac = []
        for code in function_list:
            new_rf = code
            new_refactored_code = code
            for t in range(k):
                refactors_list = [self.rename_argument,
                                  self.return_optimal,
                                  self.add_argumemts,
                                  self.rename_api,
                                  self.rename_local_variable,
                                  self.add_local_variable,
                                  self.rename_method_name,
                                  self.enhance_if,
                                  self.add_print,
                                  self.duplication,
                                  self.apply_plus_zero_math,
                                  self.dead_branch_if_else,
                                  self.dead_branch_if,
                                  self.dead_branch_while,
                                  self.dead_branch_for,
                                  # dead_branch_switch
                                  ]
                vv = 0
                while new_rf == new_refactored_code and vv <= 20:
                    try:
                        vv += 1
                        refactor = random.choice(refactors_list)
                        print('*' * 50, refactor, '*' * 50)
                        new_refactored_code = refactor(new_refactored_code)

                    except Exception as error:
                        print('error:\t', error)

                new_rf = new_refactored_code
            refac.append(new_refactored_code)

        print("refactoring finished")
        return refac



    def generate_adversarial_file_level(self,k, code):
            new_refactored_code = ''
            new_rf = code
            new_refactored_code = code
            for t in range(k):
                refactors_list = [
                                  self.rename_argument,
                                  self.return_optimal,
                                  self.add_argumemts,
                                  self.rename_api,
                                  self.rename_local_variable,
                                  self.add_local_variable,
                                  self.rename_method_name,
                                  self.enhance_if,
                                  self.add_print,
                                  self.duplication,
                                  self.apply_plus_zero_math,
                                  self.dead_branch_if_else,
                                  self.dead_branch_if,
                                  self.dead_branch_while,
                                  self.dead_branch_for
                                  ]
                vv = 0
                while new_rf == new_refactored_code and vv <= 20:
                    try:
                        vv += 1
                        refactor = random.choice(refactors_list)
                        print('*' * 50, refactor, '*' * 50)
                        new_refactored_code = refactor(new_refactored_code)
                    except Exception as error:
                        print('error:\t', error)
                new_rf = new_refactored_code
            return new_refactored_code


if __name__ == '__main__':
    K = 1
    filename = 'test.py'
    open_file = open(filename, 'r', encoding='ISO-8859-1')
    code = open_file.read()
    new_code= CodeRefactor()
    print(new_code.generate_adversarial_file_level(K,code))
