import json
import time
import openai
from openai import OpenAI
import argparse
import rich

def check_children(tree: dict):
    '''Returns true if one (or more) of tree's children are {}'''
    for value in tree.values():
        if not value: 
            return True
    return False

def compute_deepenings(tree: dict):
    '''Returns the number of deepenings needed to reach the deepest leaf'''
    deepenings = 0
    for key, subtree in tree.items():
        if isinstance(subtree, dict) and check_children(subtree):
             deepenings += 1
        else:
            deepenings += compute_deepenings(subtree)

    return deepenings

def visit_tree(tree: dict, path: list = [], progress=None):

    for key, subtree in tree.items():
        check = 0
        new_path = path + [key]     #contains the visited nodes (will NOT include the final labels)

        if isinstance(subtree, dict) and check_children(subtree):
            progress.advance(task)

            check = 1
            
            siblings = list(subtree.keys()) 
            domanda = " these classes? "
            fine2 = " every class. "
            
            inizio = " ".join(new_path)
            intro = " Amazon products can be classified as '"
            fine = "', could you give me some different more specific genres for" +domanda+ "Answer my questions in form of a python dictionary containing a list of new classes for" +fine2+ "Use double quotes for strings. Do not write comments in the code!."
            
            update_tree(tree, key, siblings, inizio, intro, fine)


        if isinstance(subtree, dict) and check==0:
            visit_tree(subtree, path=new_path, progress=progress)

    return tree

def update_tree(tree, key, siblings, inizio, intro, fine):
    n_cicli = int(len(siblings)/10)+1
    for i in range(n_cicli):
        ok = False

        while not ok:
            try:
                update_tree_step(tree, key, siblings, inizio, intro, fine, i)
                ok = True
            except SyntaxError:
                print(f"Caught Syntax Error at step {i}, retrying...")
                pass

def update_tree_step(tree, key, siblings, inizio, intro, fine, i):
    sibli = siblings[i*10:(i+1)*10]
            
    elenco = "', '".join(sibli)
                #print(f'siblings:{sibli}.')
    frase = inizio + intro + elenco + fine
                # print(frase)
                # time.sleep(15)
    
    completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are ChatGPT, a helpful AI chatbot."},
                        {"role": "user", "content": frase} 
                    ], max_tokens=1024)
                
    risposta = completion.choices[0].message.content.replace('\n','')
                # print(risposta)
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--tax", help='path for the taxonomy file', type=str, default='datastes/', required=True
    )
    parser.add_argument(
        "-k", "--key", help='your openai api-key', type=str, default=None, required=True
    )
    args = parser.parse_args()
    your_api_key = args.key
    tax_path = args.tax

    openai.api_key = your_api_key
    
    client = OpenAI(
        api_key = your_api_key
    )
    
    with open(tax_path, 'r') as file:
        tree = json.load(file)
    
    with rich.progress.Progress() as progress:
        num_deepenings = compute_deepenings(tree)
        print(f"Deepening the taxonomy by {num_deepenings} levels...")
        task = progress.add_task("[green]Deepening the taxonomy...", total=num_deepenings)
        new_tree = visit_tree(tree, progress=progress)

    with open(tax_path, 'w') as f:
        json.dump(new_tree, f)
