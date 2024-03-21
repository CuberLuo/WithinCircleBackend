def combine_strings(str1, str2):
    str1 = str(str1)
    str2 = str(str2)
    # 将给定的字符串按字母顺序排列
    sorted_strs = sorted([str1, str2])
    # 使用连字符 "-" 连接排列后的字符串
    combined_str = "-".join(sorted_strs)
    return combined_str
