def highlight_substring(string, substring):
    highlighted_string = ""
    start_index = 0
    while True:
        index = string.find(substring, start_index)
        if index == -1:
            # 如果无法找到子字符串，则将剩余的部分添加到高亮字符串中并停止循环
            highlighted_string += string[start_index:]
            break
        else:
            # 将子字符串之前的部分添加到高亮字符串中
            highlighted_string += string[start_index:index]
            # 添加高亮显示的子字符串
            highlighted_string += "\033[1;31;40m" + string[index:index+len(substring)] + "\033[0m"
            start_index = index + len(substring)

    return highlighted_string

a = highlight_substring("asdasdasd", "as")
print(a)
