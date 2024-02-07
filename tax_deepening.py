import json
import time
import openai
from openai import OpenAI
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-tax", "--tax_tree", help='path for the taxonomy file', type=str, default='datastes/', required=True
    )
    parser.add_argument(
        "-key", "--ak", help='your openai api-key', type=int, default=None, required=False
    )
    args = parser.parse_args()
    your_api_key = args.ak
    tax_path = args.tax_tree

    openai.api_key = your_api_key
    
    client = OpenAI(
        api_key = your_api_key
    )
    
    with open(tax_path, 'r') as file:
        tree = json.load(file)
    
    def visit_tree(tree: dict, path: list = []):
        for key, subtree in tree.items():
            check = 0
            new_path = path + [key]     #contains the visited nodes (will NOT include the final labels)
    
            if isinstance(subtree, dict) and check_children(subtree):
                check = 1
                
                siblings = list(subtree.keys()) 
                domanda = " these classes? "
                fine2 = " every class. "
                
                inizio = " ".join(new_path) #'"' +padre+ '"'
                intro = "Books belonging to the genre "
                intro2 = " can be classified as '"
                fine = "', could you give me some different more specific genres for" +domanda+ "Answer my questions in form of a python dictionary containing a list of new classes for" +fine2+ "Use double quotes for strings. Do not write comments in the code!."
                
                n_cicli = int(len(siblings)/10)+1
                for i in range(n_cicli):
                    sibli = siblings[i*10:(i+1)*10]
                
                    elenco = "', '".join(sibli)
                    #print(f'siblings:{sibli}.')
                    frase = intro + inizio + intro2 + elenco + fine
                    print(frase)
                    time.sleep(15)
        
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are ChatGPT, a helpful AI chatbot."},
                            {"role": "user", "content": frase} 
                        ], max_tokens=1024)
                    
                    risposta = completion.choices[0].message.content.replace('\n','')
                    print(risposta)
                    risps = risposta.split('{')
                    if len(risps)==1:
                        risposta = risps[0]
                    else: 
                        risposta = risps[1]
                    risps = risposta.split('}')
                    risposta = risps[0]
                    gpt_dict = eval("{"+risposta+"}")
        
                    for k in gpt_dict.keys():
                        try:
                            tree[key][k].update({k: {} for k in gpt_dict[k]})
                        except: print('child not found')
    
            if isinstance(subtree, dict) and check==0:
                visit_tree(subtree, new_path)
        return tree
    
    def check_children(tree: dict):
        '''Returns true if one (or more) of tree's children are {}'''
        for value in tree.values():
            if not value: 
                return True
        return False
    
    
    new = visit_tree(tree)
    
    with open(tax_path, 'w') as f:
        json.dump(tax_path, f)
