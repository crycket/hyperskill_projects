def is_once(pattern, substring):
    return pattern[0] == substring[0] or pattern[0] == '.'


def is_none_or_more(pattern, substring):
    for i, s in enumerate(substring):
        if s == pattern[0]:
            continue
        if pattern[0] != '.' or (len(pattern) > 2 and s == pattern[2]):
            return check(pattern[2:], substring[i:])
    return check(pattern[2:], '')


def is_none_or_once(pattern, substring):
    if is_once(pattern, substring):
        return check(pattern[2:], substring[1:])
    else:
        return check(pattern[2:], substring)


def is_once_or_more(pattern, substring):
    if is_once(pattern, substring):
        return is_none_or_more(pattern, substring)
    else:
        return False


def check(pattern, substring):
    if not pattern:
        return True
    if not substring:
        return False if pattern != '$' else True
    if len(pattern) > 1 and pattern[0] != '\\':
        if pattern[1] == '?':
            return is_none_or_once(pattern, substring)
        if pattern[1] == '*':
            return is_none_or_more(pattern, substring)
        if pattern[1] == '+':
            return is_once_or_more(pattern, substring)
    if pattern[0] == '\\' and pattern[1] == substring[0]:
        if len(pattern) > 2:
            if pattern[2] == '?':
                return is_none_or_once(pattern[1:], substring)
            if pattern[2] == '*':
                return is_none_or_more(pattern[1:], substring)
            if pattern[2] == '+':
                return is_once_or_more(pattern[1:], substring)
        return check(pattern[2:], substring[1:])
    if pattern[0] == '.' or pattern[0] == substring[0]:
        return check(pattern[1:], substring[1:])
    else:
        return False


def match(pattern, string):
    if not pattern:
        return True
    if pattern[0] == '^':
        return check(pattern[1:], string)
    for i in range(len(string)):
        if check(pattern, string[i:]) is True:
            return True
    return False


regex, string_to_match = input().split('|')
print(match(regex, string_to_match))
