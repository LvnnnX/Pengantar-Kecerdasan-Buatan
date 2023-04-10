#Importing
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from pathlib import Path

PATH = Path(__file__).parent
IMG_DIR = PATH / 'img'


START_STATE = {'kambing': 'asal', 'serigala': 'asal', 'sayuran': 'asal', 'perahu': 'asal'}
FINAL_STATE = {'kambing': 'tujuan', 'serigala': 'tujuan', 'sayuran': 'tujuan', 'perahu': 'tujuan'}

ATURAN = [
    {'perahu': 'tujuan', 'kambing': 'tujuan'},  # 1. perahu membawa kambing ke tujuan
    {'perahu': 'tujuan', 'sayuran': 'tujuan'},  # 2. perahu membawa sayuran ke tujuan
    {'perahu': 'tujuan', 'serigala': 'tujuan'},  # 3. perahu membawa serigala ke tujuan
    {'perahu': 'asal', 'kambing': 'asal'},  # 4. perahu membawa kambing ke asal
    {'perahu': 'asal', 'sayuran': 'asal'},  # 5. perahu membawa sayuran ke asal
    {'perahu': 'asal', 'serigala': 'asal'},  # 6. perahu membawa serigala ke asal
    {'perahu': 'asal'},  # 7. perahu kembali ke asal
    # {'perahu': 'tujuan'}  # 8. perahu jalan ke tujuan
]

def is_valid(current_state:dict) -> bool:
    #Cek apakah serigala dan kambing berada di sisi yang sama
    if current_state['serigala'] == current_state['kambing'] and current_state['perahu'] != current_state['serigala']:
    # if current_state['serigala'] == current_state['kambing']:
        return False
    #Cek apakah kambing dan sayuran berada di sisi yang sama
    if current_state['kambing'] == current_state['sayuran'] and current_state['perahu'] != current_state['kambing']:
    # if current_state['kambing'] == current_state['sayuran']:
        return False
    return True

def apply_rule(state: dict, rule: dict) -> dict:
    new_state = state.copy()
    for key, value in rule.items():
        new_state[key] = value
    return new_state

def bfs2(state: dict):
    state['tingkatan_tree'] = '0'
    df = pd.DataFrame(columns=state.keys())
    df = df.append(state, ignore_index=True)
    queue = []
    tingkatan_tree = 0
    queue.append((state, []))
    while queue:
        current_state, path = queue.pop(0)
        tingkatan_tree += 1
        del current_state['tingkatan_tree']
        if current_state == FINAL_STATE:
            # return path + [current_state]
            current_state['tingkatan_tree'] = str(tingkatan_tree)
            df = df.append(current_state, ignore_index=True)
            return df
        current_state['tingkatan_tree'] = str(tingkatan_tree)
        for num,action in enumerate(ATURAN):
            #Current state jadi acuan
            new_state = current_state.copy()
            cont_state = 0
            list_action = list(action.keys())
            list_action_value = list(action.values())
            for key,value in zip(list_action,list_action_value):
                if(current_state[key] == value):
                    cont_state = 1
                    break
                else:
                    new_state[key] = value
            if(cont_state):
                continue
            # print(ATURAN[num])
            # new_state = {**current_state, **action}
            if is_valid(new_state):
                new_path = path
                new_path.append(action)
                queue.append((new_state, new_path))
                df = df.append(new_state, ignore_index=True)
    return None

def dfs(start_state: dict, final_state: dict) -> list:
    stack = [(start_state, [])]
    visited = set()
    while stack:
        state, path = stack.pop()
        if state == final_state:
            return path + [state]
        visited.add(tuple(state.items()))
        for action in ATURAN:
            new_state = apply_rule(state, action)
            if tuple(new_state.items()) not in visited and is_valid(new_state):
                stack.append((new_state, path + [state]))
    return None

def get_bfs():
    bfs_hasil = bfs2(START_STATE)

    ax = plt.subplot(111,frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    table(ax,bfs_hasil,loc='center')
    plt.savefig(f'{IMG_DIR}/bfs.png', dpi=300, bbox_inches='tight')

def get_dfs():
    dfs_hasil = dfs(START_STATE, FINAL_STATE)
    dfs_df = pd.DataFrame(columns=dfs_hasil[0].keys())
    for i in dfs_hasil:
        dfs_df = dfs_df.append(i, ignore_index=True)
    ax = plt.subplot(111,frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    table(ax,dfs_df,loc='center')
    plt.savefig(f'{IMG_DIR}/dfs.png', dpi=300, bbox_inches='tight')
    

get_dfs()