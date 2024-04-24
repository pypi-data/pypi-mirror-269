def get_cookies_from_txt(cookies_path):
    import os
    if not os.path.exists(cookies_path):
        raise KeyError('Файл кукис не найден')
    with open(cookies_path, 'r', encoding='utf-8') as file:
        txt = file.read()

    cookies = {}

    lines = txt.splitlines()
    for line in lines:
        cookie = line.split('	')
        name = cookie[0]
        data = cookie[1]
        cookies[name] = data

    return cookies