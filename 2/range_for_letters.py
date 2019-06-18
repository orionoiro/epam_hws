def letters_range(stop, start=None, step=1, **kwargs):
    ans = []
    if not start:
        for i in range(ord('a'), ord(stop)):
            ans.append(chr(i))
    else:
        for i in range(ord(stop), ord(start), step):
            ans.append(chr(i))

    for kwarg in kwargs:
        idx = ans.index(kwarg)
        ans[idx] = kwargs[kwarg]

    return ans
