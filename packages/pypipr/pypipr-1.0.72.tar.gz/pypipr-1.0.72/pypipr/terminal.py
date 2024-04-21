import pypipr


def main():
    m = [x for x in dir(pypipr) if not x.startswith("__")]
    a = pypipr.iargv(1)
    while isinstance(m, list):
        if a is None:
            for i, v in dict(enumerate(m)).items():
                print(f"{i}. {v}")
            pypipr.print_colorize("Masukan Nomor Urut atau Nama Fungsi : ", text_end="")
            a = input()
            print()
            pypipr.exit_if_empty(len(a))

        if a.isdigit():
            m = m[int(a)]
        else:
            m = [v for v in m if v.__contains__(a)]
            pypipr.exit_if_empty(m)
            if len(m) == 1:
                m = m[0]
        a = None

    f = getattr(pypipr, m)

    pypipr.print_colorize(m)
    print(f.__doc__)

    import inspect
    s = inspect.signature(f)
    print(m, end="")
    pypipr.print_colorize(s)
    
    # a = []
    k = {}
    for i, v in s.parameters.items():
        # pypipr.print_dir(v)
        print(f"{i} [{v.default}] : ", end="")
        o = input()
        if len(o):
            # if isinstance(v.default, inspect._empty):
            #     a.append(o)
            # else:
            #     k[i] = o
            k[i] = eval(o)

    # print(a)
    print(k)
    # f(*a, **k)
    f(**k)




if __name__ == "__main__":
    main()
