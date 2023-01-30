import os
def get_files(path):
    files = []

    directory = os.listdir(path)
    directory.sort(reverse=True)

    for file in directory:
        if file.endswith('.xlsx'):
            files.append(file)
    return files

def remove_old_files(path, files):
    """ Оставляет последние 14 файлов, остальные удаляет """
    max_files = 13
    if len(files) < max_files:
        return
    i = 0
    for f in files:
        i += 1
        if i > max_files:
            os.remove(os.path.join(path, f))
            
path = 'db/'
files = get_files(path)
remove_old_files(path, files)