import random


#Class CFG_L1 implements the L1 = {a^n*b^n | n >= 0} language
class CFG_ab:
    def __init__(self):
        self.terminals = {'a', 'b'}
        self.non_terminals = {'S'}
        self.start_symbol = 'S'
        self.production_rules = {
            'S': [['a', 'S', 'b'], []]
        }

    def view(self):
        #programatic representation of CFG
        print("Terminals:", self.terminals)
        print("Non-Terminals:", self.non_terminals)
        print("Start Symbol:", self.start_symbol)
        print("Production Rules:")
        for lhs, rhs_list in self.production_rules.items():
            for rhs in rhs_list:
                print(f"{lhs} -> {''.join(rhs) if rhs else 'ε'}")

    def generate_string(self, symbol='S', max_len=10, current_string=''):
        #exceeded size
        if len(current_string) > max_len:
            return None
        
        if symbol in self.terminals:
            return current_string + symbol
        
        elif symbol == 'S':
            #choose random production
            prod = random.choice(self.production_rules['S'])
            if prod == []:
                return current_string
            else:
                left = self.generate_string('a', max_len, current_string)
                if left is None:
                    return None
                middle = self.generate_string('S', max_len, left)
                if middle is None:
                    return None
                right = self.generate_string('b', max_len, middle)
                return right
        else:
            return current_string

    def generate_strings(self, string_no=10, max_len=20):
        #string generator
        ans = set()
        attempts = 0

        #generate string_no distinct strings
        while len(ans) < string_no:
            generated = self.generate_string(max_len=max_len)
            if generated is not None and len(generated) <= max_len:
                ans.add(generated)
            attempts += 1

        print('Generated strings are:', ','.join(list(ans))[1:])
        return list(ans)
    
    def derive(self, target, current='S', derivation_steps=None):
        if derivation_steps is None:
            derivation_steps = [current]

        #current matches target
        if current == target:
            return derivation_steps

        #exceeded size of target -> wrong production
        min_possible = current.replace('S', '')
        if len(min_possible) > len(target):
            return None

        #expand S
        s_index = current.find('S')
        if s_index == -1:
            return None

        for prod in self.production_rules['S']:
            #replace S with a production
            replacement = ''.join(prod) if prod else ''
            new_string = current[:s_index] + replacement + current[s_index+1:]

            result = self.derive(target, new_string, derivation_steps + [new_string])
            if result:
                return result
        return None
    
    def show_derivation(self, target):
        #shows a derivation
        steps = cfg.derive(target)
        if steps:
            print(' -> '.join(steps))

    def check_membership(self, string):
        #check if a given string is member of our particular CFG
        #in this case we simply check that |a| = |b| and a's before b's
        if string == "":
            return True
        
        if len(string) < 2:
            return False
        
        if string[0] == 'a' and string[-1] == 'b':
            return self.check_membership(string[1:-1])
        
        return False

#Class CFG_abc implements the L = {a^n*b^n*c^n | n >= 0} language
class CFG_abc:
    def __init__(self):
        self.terminals = {'a', 'b', 'c'}
        self.non_terminals = {'S'}
        self.start_symbol = 'S'
        self.production_rules = {
            'S': [['a', 'S', 'b', 'c'], ['a', 'b', 'c']]
        }

    def is_member(self, string):
        #simply check if |a| == |b| == |c| and a before b before c
        if len(string) % 3 != 0 or len(string) == 0:
            return False
        n = len(string) // 3
        return string[:n] == 'a' * n and string[n:2*n] == 'b' * n and string[2*n:] == 'c' * n

    def generate_string(self, symbol='S', max_depth=10, current_depth=0):
        #choose a random production if nor max_depth yet
        if current_depth > max_depth:
            production = ['a', 'b', 'c']
        else:
            production = random.choice(self.production_rules[symbol])

        result = ""
        for sym in production:
            if sym in self.terminals:
                result += sym
            elif sym in self.non_terminals:
                result += self.generate_string(sym, max_depth, current_depth + 1)
        return result
        

    def generate_strings(self, count=10, max_depth=10):
        #generate strings function
        ans = set()
        while len(ans) < count:
            s = self.generate_string(max_depth=max_depth)
            ans.add(s)
        
        print('Generated strings are:', ','.join(list(ans))[1:])
        return list(ans)

if __name__ == '__main__':
    cfg = CFG_ab()
    generated = cfg.generate_strings()
    cfg.show_derivation('aaaabbbb')
    print(cfg.check_membership('abb'))

    cf = CFG_abc()
    generated = cf.generate_strings()
    
    


