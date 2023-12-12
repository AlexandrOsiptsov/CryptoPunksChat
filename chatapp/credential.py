file_path = "chatapp/all_credits.txt"

def clear_file():
    global file_path
    with open(file_path, "w") as file:
        file.truncate()

def add_aes_key( key, value):
    global file_path
    with open(file_path, 'a') as file:
        file.write(f'{key} {value}\n')

def get_aes_key( key):
    global file_path
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            if len(parts) == 2 and parts[0] == key:
                return parts[1]
    return None

def update_aes_key( key, new_value):
    global file_path
    lines = []
    updated = False

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            if len(parts) == 2 and parts[0] == key:
                lines.append(f'{key} {new_value}\n')
                updated = True
            else:
                lines.append(line)

    if updated:
        with open(file_path, 'w') as file:
            file.writelines(lines)

def delete_aes_key( key):
    global file_path
    lines = []
    deleted = False

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            if len(parts) == 2 and parts[0] == key:
                deleted = True
            else:
                lines.append(line)

    if deleted:
        with open(file_path, 'w') as file:
            file.writelines(lines)