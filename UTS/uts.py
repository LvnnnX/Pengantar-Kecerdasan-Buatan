import pandas as pd

pd.set_option('display.max_columns', None)

START_STATE = {'petani': 'asal', 'kambing': 'asal', 'serigala': 'asal', 'sayuran': 'asal', 'perahu':'asal'}

user_input = {}
valid_input = ['0','1','asal','tujuan']

print("""

    ========================================
    | Program nyebrang                     |
    ========================================
    Input lokasi awal dengan :
    0/asal = di sisi awal
    1/tujuan = di sisi tujuan

""")

for i in (START_STATE.keys()):
    while True:
        try:
            get_input = input(f'Input lokasi {i.capitalize()}: ')
            if get_input in valid_input:
                user_input[i] = valid_input[valid_input.index(get_input)%2+2]
                break
            else:
                raise ValueError
        except ValueError:
            print('Input harus asal atau tujuan')

if(user_input['perahu'] != user_input['petani']):
    print('Perahu harus berada di sisi yang sama dengan petani')

START_STATE = dict(START_STATE, **user_input)
print(START_STATE)

FINAL_STATE = {'petani': 'tujuan', 'kambing': 'tujuan', 'serigala': 'tujuan', 'sayuran': 'tujuan', 'perahu':'tujuan'}

ATURAN = [
    {'petani': 'tujuan', 'kambing': 'tujuan', 'perahu' : 'tujuan'},  # 1. petani membawa kambing ke tujuan
    {'petani': 'tujuan', 'sayuran': 'tujuan', 'perahu' : 'tujuan'},  # 2. petani membawa sayuran ke tujuan
    {'petani': 'tujuan', 'serigala': 'tujuan','perahu' : 'tujuan'},  # 3. petani membawa serigala ke tujuan
    {'petani': 'asal', 'kambing': 'asal','perahu' : 'asal'},  # 4. petani membawa kambing ke asal
    {'petani': 'asal', 'sayuran': 'asal','perahu' : 'asal'},  # 5. petani membawa sayuran ke asal
    {'petani': 'asal', 'serigala': 'asal','perahu' : 'asal'},  # 6. petani membawa serigala ke asal
    {'petani': 'asal','perahu' : 'asal'},  # 7. petani kembali ke asal
    {'petani': 'tujuan','perahu' : 'tujuan'}  # 8. petani jalan ke tujuan
]

def is_valid(current_state:dict) -> bool:
    #Cek apakah serigala dan kambing berada di sisi yang sama
    if current_state['serigala'] == current_state['kambing'] and current_state['petani'] != current_state['serigala']:
        return False
    #Cek apakah kambing dan sayuran berada di sisi yang sama
    if current_state['kambing'] == current_state['sayuran'] and current_state['petani'] != current_state['kambing']:
        return False
    return True

def petani_check(current_state:dict, rule:dict) -> bool:
    if 'petani' in current_state.keys():
        if current_state['petani'] != rule['petani']:
            return True
    return False

def dfs(state:dict | None = START_STATE, visited:set | None = set()) -> list | None:
    stack = [(state, [])]
    # print(state,'inistate')
    while stack:
        current_state, path = stack.pop()
        if current_state == FINAL_STATE:
            # print('returning', path,current_state)
            return path + [current_state]
        visited.add(tuple(current_state.items()))
        for rule in ATURAN:
            if(petani_check(current_state,rule) and is_valid(new_state:=dict(current_state, **rule))):
                if tuple(new_state.items()) not in visited:
                    stack.append((new_state, path + [current_state]))
    return None

solution = dfs()

if solution != None:
    df = pd.DataFrame(columns=list(START_STATE.keys()))
    for i in solution:
        # df = df.append(i, ignore_index=True)
        df.loc[len(df.index)] = i
    # print(*dfs(START_STATE),sep='\n')
    df.rename(str.capitalize, axis='columns', inplace=True)
    print(df.to_markdown())
else:
    print('Tidak ada solusi')