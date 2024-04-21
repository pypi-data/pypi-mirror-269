# Tool/Java_refactor
# java_test.java
# generate_refactoring.py
# processing_source_code.py 
# refactoring_methods.py
# util.py


import random, wordninja, wordnet, re, json, javalang, secrets
from shutil import copyfile
from nltk.corpus import wordnet
from genericpath import isfile
from processing_source_code import extract_argument, extract_brace, extract_class, extract_for_loop,extract_function, extract_if, extract_local_variable, extract_method_name, word_synonym_replacement
from refactoring_methods import add_argumemts, add_local_variable, add_print, apply_plus_zero_math, dead_branch_for, dead_branch_if, dead_branch_if_else, dead_branch_switch, dead_branch_while, duplication, enhance_if, rename_api, rename_argument, rename_local_variable, rename_method_name, return_optimal
from util import format_code_chuncks, get_branch_for_mutant, get_branch_if_else_mutant, get_branch_if_mutant, get_branch_switch_mutant, get_branch_while_mutant, get_dead_for_condition, get_local_vars, get_radom_var_name, get_random_false_stmt, get_random_int, get_random_type_name_and_value_statment, get_tree
from os import listdir
from os.path import isfile, join
from util import *
from processing_source_code import *
from refactoring_methods import *




reserved_kws = ["abstract", "assert", "boolean",
                "break", "byte", "case", "catch", "char", "class", "const",
                "continue", "default", "do", "double", "else", "extends", "false",
                "final", "finally", "float", "for", "goto", "if", "implements",
                "import", "instanceof", "int", "interface", "long", "native",
                "new", "null", "package", "private", "protected", "public",
                "return", "short", "static", "strictfp", "super", "switch",
                "synchronized", "this", "throw", "throws", "transient", "true",
                "try", "void", "volatile", "while"]

reserved_cls = ["ArrayDeque", "ArrayList", "Arrays", "BitSet", "Calendar", "Collections", "Currency",
                "Date", "Dictionary", "EnumMap", "EnumSet", "Formatter", "GregorianCalendar", "HashMap",
                "HashSet", "Hashtable", "IdentityHashMap", "LinkedHashMap", "LinkedHashSet",
                "LinkedList", "ListResourceBundle", "Locale", "Observable",
                "PriorityQueue", "Properties", "PropertyPermission",
                "PropertyResourceBundle", "Random", "ResourceBundle", "ResourceBundle.Control",
                "Scanner", "ServiceLoader", "SimpleTimeZone", "Stack",
                "StringTokenizer", "Timer", "TimerTask", "TimeZone",
                "TreeMap", "TreeSet", "UUID", "Vector", "WeakHashMap"
                ]

reserved_kws = reserved_kws + reserved_cls

    




class java_setup :

    # generate_refactoring.py
    def return_function_code(self, code, method_names):
        final_codes = []
        final_names = []

        Class_list, raw_code = extract_class(code)

        for class_name in Class_list:
            function_list, class_name = extract_function(class_name)

        for fun_code in function_list:

            for method_name in method_names:
                method_name_tem = method_name.replace('|', '')
                if method_name_tem.upper() in fun_code.split('\n')[0].upper():

                    final_codes.append(fun_code)
                    final_names.append(method_name)

        return final_codes, final_names


    def generate_adversarial(self, k, code, method_names):

            method_name = method_names[0]
            function_list = []
            class_name = ''

            Class_list, raw_code = extract_class(code)

            for class_name in Class_list:
                function_list, class_name = extract_function(class_name)

            refac = []
            new_refactored_code = ''

            for code in function_list:
                if method_name not in code.split('\n')[0]:
                    continue

                new_rf = code
                new_refactored_code = code

                # print(code)
                for t in range(k):
                    refactors_list = [rename_argument,
                                      return_optimal,
                                      add_argumemts,
                                      rename_api,
                                      rename_local_variable,
                                      add_local_variable,
                                      rename_method_name,
                                      enhance_if,
                                      add_print,
                                      duplication,
                                      apply_plus_zero_math,
                                      dead_branch_if_else,
                                      dead_branch_if,
                                      dead_branch_while,
                                      dead_branch_for,
                                      dead_branch_switch
                                      ]

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


    def generate_adversarial_json(self, k, code):
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

                refactors_list = [rename_argument,
                                  return_optimal,
                                  add_argumemts,
                                  rename_api,
                                  rename_local_variable,
                                  add_local_variable,
                                  rename_method_name,
                                  enhance_if,
                                  add_print,
                                  duplication,
                                  apply_plus_zero_math,
                                  dead_branch_if_else,
                                  dead_branch_if,
                                  dead_branch_while,
                                  dead_branch_for,
                                  dead_branch_switch
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


    def generate_adversarial_file_level(self, k, code):
            new_refactored_code = ''
            new_rf = code
            new_refactored_code = code

            for t in range(k):
                refactors_list = [rename_argument,
                                  return_optimal,
                                  add_argumemts,
                                  rename_api,
                                  rename_local_variable,
                                  add_local_variable,
                                  rename_method_name,
                                  enhance_if,
                                  add_print,
                                  duplication,
                                  apply_plus_zero_math,
                                  dead_branch_if_else,
                                  dead_branch_if,
                                  dead_branch_while,
                                  dead_branch_for,
                                  dead_branch_switch
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

       
       # processing_source_code.py
    def word_synonym_replacement(self, word):
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
            word_new = random.choice(word_ret)
        except:
            word_new = word


        return word.replace(word_tar,word_new),word_ret


    def extract_method_name(self, string):
        match_ret = re.search('\w+\s*\(',string)
        if match_ret:
            method_name = match_ret.group()[:-1].strip()
            return method_name
        else:
            return None


    def extract_argument(self, string):
        end_pos    = string.find('{')
        sta_pas    = string.find('(')
        arguments  = string[sta_pas + 1 :end_pos].strip()[:-1]
        arguments_list = arguments.split(',')
        if ' ' in arguments_list:
            arguments_list.remove(' ')
        if '' in arguments_list:
            arguments_list.remove('')
        return arguments_list


    def extract_brace(self, string,start_pos):
        length = 0
        brace_l_num = 0
        brace_r_num = 0
        for char in string[start_pos:]:
            if char == '{':
                brace_l_num += 1
            if char == '}':
                brace_r_num += 1
            if brace_l_num == brace_r_num and brace_l_num > 0:
                break;
            length += 1
        return string[start_pos: start_pos + length + 1]

    '''
    def extract_import(string):
        import_list = re.findall('import .+;',string)
        return import_list,string
    '''


    def extract_class(self, string):

        class_list = []
        while ' class ' in string:
            start_pos  = string.find(' class ')
            class_text = extract_brace(string, start_pos)
            class_list.append(class_text)
            string = string.replace(class_text,'')

        return class_list,string


    def extract_member_variable(self, string):

        variable_list = []
        while True:
            match_ret = re.search('(private|public).+;', string)
            if match_ret:
                variable_text = match_ret.group()
                variable_list.append(variable_text)
                string = string.replace(variable_text,'')
            else:
                break
        return variable_list,string


    def extract_function(self, string):
        i = 0
        function_list = []
        while True:
            match_ret = re.search('(protected|private|public).+\s*{', string)
            if match_ret:
                function_head = match_ret.group()
                start_pos = string.find(function_head)
                function_text = extract_brace(string, start_pos)
                function_list.append(function_text)
                string = string.replace(function_text, 'vesal'+ str(i))
                i+=1
            else:
                break
        return function_list, string


    def extract_for_loop(self, string):

        for_list = []
        while True:
            match_ret = re.search('for\s+\(', string)
            print(match_ret)
            if match_ret:
                for_head = match_ret.group()
                start_pos = string.find(for_head)
                for_text = extract_brace(string, start_pos)
                for_list.append(for_text)
                string = string.replace(for_text, '')
            else:
                break
        return for_list


    def extract_if(self, string):

        if_list = []
        while True:
            match_ret = re.search('if\s+\(', string)
            if match_ret:
                if_head = match_ret.group()
                start_pos = string.find(if_head)
                if_text = extract_brace(string, start_pos)
                if_list.append(if_text)
                string = string.replace(if_text, '')
            else:
                break
        return if_list


    def extract_while_loop(self, string):

        while_list = []
        while True:
            match_ret = re.search('while\s+\(', string)
            if match_ret:
                while_head = match_ret.group()
                start_pos = string.find(while_head)
                while_text = extract_brace(string, start_pos)
                while_list.append(while_text)
                string = string.replace(while_text, '')
            else:
                break
        return while_list, string


    def extract_local_variable(self, string):

        local_var_list = []
        statement_list = string.split('\n')
        for line in statement_list:
            match_ret = re.search('[^\s]+\s+\w+\s+=', line)
            if match_ret:
                var_definition = match_ret.group()
                local_var_list.append(var_definition.split(' ')[1])

        return local_var_list
    

    def rename_local_variable(self, method_string):
        local_var_list = extract_local_variable(method_string)
        if len(local_var_list) == 0:
            return method_string

        mutation_index = random.randint(0, len(local_var_list) - 1)
        return method_string.replace(local_var_list[mutation_index], word_synonym_replacement(local_var_list[mutation_index])[0])


    def add_local_variable(self, method_string):
        local_var_list = extract_local_variable(method_string)
        if len(local_var_list) == 0:
            return method_string

        mutation_index = random.randint(0, len(local_var_list) - 1)
        match_ret      = re.search('.+' + local_var_list[mutation_index] + '.+;', method_string)
        if match_ret:
            var_definition      = match_ret.group()
            new_var_definition  = var_definition.replace(local_var_list[mutation_index], word_synonym_replacement(local_var_list[mutation_index])[0])
            method_string       = method_string.replace(var_definition, var_definition + '\n' + new_var_definition)
            return method_string
        else:
            return method_string


    def duplication(self, method_string):
        local_var_list = extract_local_variable(method_string)
        if len(local_var_list) == 0:
            return method_string
        mutation_index = random.randint(0, len(local_var_list) - 1)
        match_ret = re.search('.+' + local_var_list[mutation_index] + '.+;', method_string)
        if match_ret:
            var_definition = match_ret.group()
            new_var_definition = var_definition
            method_string = method_string.replace(var_definition, var_definition + '\n' + new_var_definition)
            # print(method_string)
            return method_string
        else:
            # print(method_string)
            return method_string


    def rename_api(self, method_string):
        match_ret      = re.findall('\.\s*\w+\s*\(', method_string)
        if match_ret != []:
            api_name = random.choice(match_ret)[1:-1]
            return method_string.replace(api_name,word_synonym_replacement(api_name)[0])
        else:
            return method_string


    def rename_method_name(self, method_string):
        method_name = extract_method_name(method_string)
        if method_name:
            return method_string.replace(method_name, word_synonym_replacement(method_name)[0])
        else:
            return method_string


    def rename_argument(self, method_string):
        arguments_list = extract_argument(method_string)
        if len(arguments_list) == 0:
            return method_string

        mutation_index = random.randint(0, len(arguments_list) - 1)
        # print(method_string.replace(arguments_list[mutation_index],word_synonym_replacement(arguments_list[mutation_index])[0]))
        return method_string.replace(arguments_list[mutation_index],word_synonym_replacement(arguments_list[mutation_index])[0])


    def return_optimal(self, method_string):
        if 'return ' in method_string:
            return_statement  = method_string[method_string.find('return ') : method_string.find(';', method_string.find('return ') + 1)]
            return_object     = return_statement.replace('return ','')
            if return_object == 'null':
                return method_string
            optimal_statement = 'if (' + return_object + ' == null){\n\t\t\treturn 0;\n\t\t}\n' + return_statement
            method_string = method_string.replace(return_statement, optimal_statement)
        return method_string


    def enhance_for_loop(self, method_string):
        for_loop_list = extract_for_loop(method_string)
        if for_loop_list == []:
            return method_string
        mutation_index = random.randint(0, len(for_loop_list) - 1)
        for_text = for_loop_list[mutation_index]
        for_info = for_text[for_text.find('(') + 1 : for_text.find(')')]
        for_body = for_text[for_text.find('{') + 1 : for_text.rfind('}',-1,10)]
        if ':' in for_info:
            loop_bar = for_info.split(':')[-1].strip()
            loop_var = for_info.split(':')[0].strip().split(' ')[-1].strip()
            if loop_bar == None or loop_bar == '' or loop_var == None or loop_var == '':
                return method_string
            new_for_info = 'int i = 0; i < ' + loop_bar + '.size(); i ++'
            method_string = method_string.replace(for_info, new_for_info)
            method_string = method_string.replace(for_body,for_body.replace(loop_var, loop_bar + '.get(i)'))

            return method_string

        else:
            return method_string


    def add_print(self, method_string):
        statement_list = method_string.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement      = statement_list[mutation_index]
        new_statement  = '\t' + 'System.out.println("' + str(random.choice(word_synonym_replacement(statement)[1])) + '");'
        method_string = method_string.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def enhance_if(self, method_string):
        if_list = extract_if(method_string)
        mutation_index = random.randint(0, len(if_list) - 1)
        if_text = if_list[mutation_index]
        if_info = if_text[if_text.find('(') + 1 :if_text.find('{')][:if_text.rfind(')',-1,5) -1]
        new_if_info = if_info
        if 'true' in if_info:
            new_if_info = if_info.replace('true','(0==0)')
        if 'flase' in if_info:
            new_if_info = if_info.replace('flase','(1==0)')
        if '!' in if_info and '!=' not in if_info and '(' not in if_info and '&&' not in if_info and '||' not in if_info:
            new_if_info = if_info.replace('!', 'flase == ')
        if '<' in if_info and '<=' not in if_info and '(' not in if_info and '&&' not in if_info and '||' not in if_info:
            new_if_info = if_info.split('<')[1] + ' > ' + if_info.split('<')[0]
        if '>' in if_info and '>=' not in if_info and '(' not in if_info and '&&' not in if_info and '||' not in if_info:
            new_if_info = if_info.split('>')[1] + ' < ' + if_info.split('>')[0]
        if '<=' in if_info and '(' not in if_info and '&&' not in if_info and '||' not in if_info:
            new_if_info = if_info.split('<=')[1] + ' >= ' + if_info.split('<=')[0]
        if '>=' in if_info and '(' not in if_info and '&&' not in if_info and '||' not in if_info:
            new_if_info = if_info.split('>=')[1] + ' <= ' + if_info.split('>=')[0]
        if '.equals(' in if_info:
            new_if_info = if_info.replace('.equals', '==')

        return method_string.replace(if_info,new_if_info)


    def add_argumemts(self, method_string):
        arguments_list = extract_argument(method_string)
        arguments_info = method_string[method_string.find('(') : method_string.find('{')]
        if len(arguments_list) == 0:
            arguments_info = 'String ' + word_synonym_replacement(extract_method_name(method_string))[0]
            return method_string[0 : method_string.find('()') + 1] + arguments_info + method_string[method_string.find('()') + 1 :]
        mutation_index = random.randint(0, len(arguments_list) - 1)
        org_argument = arguments_list[mutation_index]
        new_argument = word_synonym_replacement(arguments_list[mutation_index])[0]
        new_arguments_info = arguments_info.replace(org_argument,org_argument + ', ' + new_argument)
        method_string = method_string.replace(arguments_info,new_arguments_info)
        return method_string


    def enhance_filed(self, method_string):
        arguments_list = extract_argument(method_string)
        if len(arguments_list) == 0:
            return method_string
        mutation_index = random.randint(0, len(arguments_list) - 1)
        extra_info = "\n\tif (" + arguments_list[mutation_index].strip().split(' ')[-1] + " == null){\n\t\tSystem.out.println('please check your input');\n\t}"
        method_string = method_string[0 : method_string.find(';') + 1] + extra_info + method_string[method_string.find(';') + 1 : ]
        return method_string


    def apply_plus_zero_math(self, data):

        statement_list = data.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]

        tree = get_tree(data)
        var_list = get_local_vars(tree)
        var_list = [var for var, var_type in var_list if var_type in (
            "int", "float", "double", "long")]
        if var_list==[]:
            return ""
        for var in var_list:
            mutant = ' ' + str(var) + ' = ' + str(var) + ' + ' + str(0) + ";"

            for idx, _ in enumerate(statement_list):
                if var in _ and idx < len(statement_list) - 1:
                    insertion_index = idx + 1
            method_string = data.replace(statement, '\n' + mutant + '\n' + statement)
        return method_string




    def dead_branch_if_else(self, data):
        statement_list = data.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        new_statement = get_branch_if_else_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        # print(method_string)
        return method_string
        # return data


    def dead_branch_if(self, data):

        statement_list = data.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        new_statement = get_branch_if_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def dead_branch_while(self, data):

        statement_list = data.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        new_statement = get_branch_while_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def dead_branch_for(self, data):

        statement_list = data.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        new_statement = get_branch_for_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def dead_branch_switch(self, data):

        statement_list = data.split(';')
        mutation_index = random.randint(1, len(statement_list) - 1)
        statement = statement_list[mutation_index]
        new_statement = get_branch_switch_mutant()
        method_string = data.replace(statement, '\n' + new_statement + '\n' + statement)
        return method_string


    def get_radom_var_name(self):
        res_string = ''
        for x in range(8):
            res_string += random.choice('abcdefghijklmnopqrstuvwxyz')
        return res_string


    def get_dead_for_condition(self):
        var = get_radom_var_name()
        return "int "+var+" = 0; "+var+" < 0; "+var+"++"


    def get_random_false_stmt(self):
        res = [random.choice(["true", "false"]) for x in range(10)]
        res.append("false")
        res_str = " && ".join(res)
        return res_str


    def get_tree(self, data):
        tokens = javalang.tokenizer.tokenize(data)
        parser = javalang.parser.Parser(tokens)
        tree = parser.parse_member_declaration()
        return tree


    def verify_method_syntax(self, data):
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
        var_name = get_radom_var_name()

        if datatype == "byte":
            var_value = get_random_int(-128, 127)
        elif datatype == "short":
            var_value = get_random_int(-10000, 10000)
        elif datatype == "boolean":
            var_value = random.choice(["true", "false"])
        elif datatype == "char":
            var_value = str(random.choice(
                'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')))
            var_value = '"'+var_value+'"'
        elif datatype == "String":
            var_value = str(get_radom_var_name())
            var_value = '"'+var_value+'"'
        else:
            var_value = get_random_int(-1000000000, 1000000000)

        mutant = str(datatype) + ' ' + str(var_name) + ' = ' + str(var_value)+";"
        return mutant


    def generate_file_name_list_file_from_dir(self, method_path):
        filenames = [f for f in listdir(
            method_path) if isfile(join(method_path, f))]
        with open(method_path+'\\'+'all_file_names.txt', 'w') as f:
            f.write(json.dumps(filenames))
        print("done")


    def get_file_name_list(self, method_path):
        with open(method_path+'\\'+'all_file_names.txt') as f:
            data = json.load(f)
        return data


    def get_random_int(self, min, max):
        return random.randint(min, max)


    def format_code_chuncks(self, code_chuncks):
        for idx, c in enumerate(code_chuncks):
            c = c.replace(' . ', '.')
            c = c.replace(' ( ', '(')
            c = c.replace(' ) ', ')')
            c = c.replace(' ;', ';')
            c = c.replace('[ ]', '[]')
            code_chuncks[idx] = c
        return code_chuncks


    def format_code(self, c):
        c = c.replace(' . ', '.')
        c = c.replace(' ( ', '(')
        c = c.replace(' ) ', ')')
        c = c.replace(' ;', ';')
        c = c.replace('[ ]', '[]')
        return c


    def get_method_header(self, string):
        method_header = ''
        tree = get_tree(string)
        # print("tree")

        tokens = list(javalang.tokenizer.tokenize(string))
        # print(tokens)
        chunck_start_poss = [s.position.column for s in tree.body]
        # print(chunck_start_poss)
        if len(chunck_start_poss) > 0:
            method_header = ' '.join([t.value for t in tokens
                                    if t.position.column < chunck_start_poss[0]])

        method_header = format_code_chuncks([method_header])[0]
        return method_header


    def get_method_statement(self, string):
        code_chuncks = []
        tree = get_tree(string)
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
        code_chuncks = format_code_chuncks(code_chuncks)
        return code_chuncks


    def scan_tree(self, tree):
        for path, node in tree:
            print("=======================")
            print(node)


    def get_all_type(self, tree):
        res_list=[]
        for path, node in tree.filter(javalang.tree.ReferenceType):
            if node.name != None:
                res_list.append(node.name)
        return list(set(res_list))


    def scan_local_vars(self, tree):
        for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
            print("name=========type=============")
            print(node.declarators[0].name, "\t", node.type.name)


    def get_local_vars(self, tree):
        var_list = []
        for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
            var_list.append([node.declarators[0].name, node.type.name])

        return var_list


    def get_local_assignments(self, tree):
        var_list = []
        for path, node in tree.filter(javalang.tree.Assignment):
            var_list.append([node.declarators[0].name, node.type.name])
        return var_list


    def get_branch_if_else_mutant(self):
        mutant = 'if ('+get_random_false_stmt()+') {' + \
            get_random_type_name_and_value_statment() + \
            '}' + \
            'else{' + \
            get_random_type_name_and_value_statment() + \
            '}'
        return mutant


    def get_branch_if_mutant(self):
        mutant = 'if ('+get_random_false_stmt()+') {' + \
            get_random_type_name_and_value_statment() + \
            '}'
        return mutant


    def get_branch_while_mutant(self):
        mutant = 'while ('+get_random_false_stmt()+') {' + \
            get_random_type_name_and_value_statment() + \
            '}'
        return mutant


    def get_branch_for_mutant(self):
        dead_for_condition = get_dead_for_condition()
        mutant = 'for  ('+dead_for_condition+') {' + \
            get_random_type_name_and_value_statment() + \
            '}'
        return mutant

    def get_branch_switch_mutant(self):
        var_name = get_radom_var_name()
        mutant = 'int ' + var_name+' = 0;' +\
            'switch  ('+var_name+') {' + \
            'case 1:' + \
            get_random_type_name_and_value_statment() + \
            'break;' +\
            'default:' + \
            get_random_type_name_and_value_statment() + \
            'break;' +\
            '}'
        return mutant


