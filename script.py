def muldiv(a):
    a = a.replace(' ', '')
    num = []
    oper = []
    mn = a[0]
    for i in range(1, len(a)):
        count_l, count_r = mn.count('('), mn.count(')')
        if a[i] in '.0123456789()' or count_r != count_l:
            mn += a[i]
        else:
            if '(' in mn and ')' in mn:
                num.append(float(mn[1:len(mn)-1]))
            else:
                num.append(float(mn))
            oper.append(a[i])
            mn = ''
    if '(' in mn and ')' in mn:
        num.append(float(mn[1:len(mn) - 1]))
    else:
        num.append(float(mn))
    mult = num[0]
    for i in range(1, len(num)):
        if oper[i-1] == '*':
            mult *= num[i]
        if oper[i-1] == '/':
            mult /= num[i]
    return mult


def addsub(b):
    if not '+' in b and not '-' in b:
        return muldiv(b)
    b = b.replace(' ', '')
    numb = []
    operations = []
    slg = b[0]
    for i in range(1, len(b)):
        count_l, count_r = slg.count('('), slg.count(')')
        if (b[i] in '.0123456789*/()' or count_l != count_r) and (count_l <= 1 and count_r <= 1):
            slg += b[i]
        else:
            if '*' in slg or '/' in slg:
                numb.append(muldiv(slg))
            elif '(' in slg and ')' in slg:
                numb.append(float(slg[1:len(slg)-1]))
            else:
                numb.append(float(slg))
            operations.append(b[i])
            slg = ''
    if '*' in slg or '/' in slg:
        numb.append(muldiv(slg))
    elif ('(' and ')') in slg:
        numb.append(float(slg[1:len(slg)-1]))
    else:
        numb.append(float(slg))
    summ = numb[0]
    for i in range(1, len(numb)):
        if operations[i-1] == '+':
           summ += numb[i]
        if operations[i-1] == '-':
            summ -= numb[i]
    return summ


def reshaka(strc):
    strc = strc.replace(' ', '')
    usl_main = True
    frg_test = ''
    count_l = 0
    count_r = 0
    for i in range(len(strc)):
        if strc[i] == '(':
            count_l += 1
        if strc[i] == ')':
            count_r += 1
        if count_l != count_r:
            frg_test += strc[i]
        elif frg_test != '':
            usl_1 = frg_test.count('*') + frg_test.count('/') > 0 or frg_test.count('+') + frg_test.count('-') > 1
            usl_2 = frg_test[1] in '1234567890.' and frg_test.count('*') + frg_test.count('/') + frg_test.count('+') + frg_test.count('-') > 0
            if usl_1 or usl_2:
                usl_main = False
                break
            frg_test = ''
            count_r = count_l = 0
    if usl_main is True:
        return addsub(strc)
    else:
        frg = ''
        count_r = count_l = 0
        primer = strc
        for i in range(len(primer)):
            if primer[i] == '(':
                count_l += 1
            if primer[i] == ')':
                count_r += 1
            if count_l != count_r:
                frg += primer[i]
            elif frg != '':
                lol = reshaka(frg[1:])
                if float(lol) < 0:
                    strc = primer.replace(frg+')', '('+str(lol)+')', 1)
                else:
                    strc = primer.replace(frg+')', str(lol), 1)
                count_r = count_l = 0
                frg = ''
    return reshaka(strc)


File_in = open("input.txt")
File_out = open("output.txt", 'w')

strochka = File_in.readline()
strochka = strochka.replace('\n', '')

File_out.write(str(reshaka(strochka)))

File_in.close()
File_out.close()
print('done')
