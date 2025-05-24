# CFGParser
Parser for context-free grammars. The program manages the CFG that models the langauge L = { aⁿ bⁿ | n ≥ 0 }
## CFG Definition
Create a programmatic representation of the following: S → aSb | ε <br>
In the program a CFG is represented like this:
```
self.terminals = {'a', 'b'} #set
self.non_terminals = {'S'} #set
self.start_symbol = 'S' 
self.production_rules = { #dict
'S': [['a', 'S', 'b'], []]
}
```
## String Generator
To generate string the program chooses a random production and continues the process until a maximum length 
is reached. Then, there is another function that generates a set of distinct strings that belong to the language. 
```
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
```
For example, `CFG_ab().generate_strings(5)` returns maximum 5 strings of max_len 20: `Generated strings are: ab,aabb,aaaaaaabbbbbbb,aaabbb`.

## Derivations
Given a target string, the program determines it's derivation. For example, given the string `aaaabbbb`, the output is of the form: `S -> aSb -> aaSbb -> aaaSbbb -> aaaaSbbbb -> aaaabbbb`. This is done by starting from the start symbol and expanding the leftmost non-terminal, a leftmost derivation.
```
#expand S (leftmost derivation)
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
```

## Membership Tester
Membership testing for a general CFG is usually done by implementing CYK or Earley parsers. In the application, as the language we are modelling is 
straight-forward, the membership tester is implemented by simply checking that the number of a's is equal to the number of b's and that b's precede a's. The implementation is recursive and is self-explanatory.
```
def check_membership(self, string):
    if string == "":
        return True
    
    if len(string) < 2:
        return False
    
    if string[0] == 'a' and string[-1] == 'b':
        return self.check_membership(string[1:-1])
    
    return False
```
## Extending the CFG
### Model
Extending the CFG to model the language:
L' = { aⁿ bⁿ cⁿ | n ≥ 0 }. This langauge can't be modeled by a CFG. Even if this is true, we can try to model it using the following CFG:
S → aSbSc | a | b | c. This CFG might generate strings like: `aabbcc`, `aaabbbccc`, it also outputs wrong string like: `aabcbabccbabcc`.
This language can't be modeled by a CFG. This can be proven using pumping lemma for CFG. <br>
String generation works just like above. The form of the CFG is as follows:
```
self.terminals = {'a', 'b', 'c'}
self.non_terminals = {'S'}
self.start_symbol = 'S'
self.production_rules = {
    'S': [['a', 'S', 'b', 'S', 'c'], ['a', 'b', 'c']]
}
```
### Recognizer
Just like the membership checker from above, a recognizer for words included in this language is straight forward:
```
def check_membership(self, string):
    #simply check if |a| == |b| == |c| and a before b before c
    if len(string) % 3 != 0 or len(string) == 0:
      return False
    n = len(string) // 3
    return string[:n] == 'a' * n and string[n:2*n] == 'b' * n and string[2*n:] == 'c' * n
```
## Running instructions
Python3 is required for this application. To execute the CFG parser, simply run `main.py`:
```
python3 main.py
```

