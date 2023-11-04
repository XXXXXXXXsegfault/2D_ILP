has_maximum = 0
has_minimum = 0
maximum = 0
minimum = 0
def div_up(a,b):
    value = a // b
    if b > 0:
        while value * b > a:
            value -= 1
        while value * b < a:
            value += 1
    else:
        while value * b < a:
            value -= 1
        while value * b > a:
            value += 1
    return value
def div_down(a,b):
    value = a // b
    if b > 0:
        while value * b < a:
            value += 1
        while value * b > a:
            value -= 1
    else:
        while value * b > a:
            value += 1
        while value * b < a:
            value -= 1
    return value
# b1*n >= a1*m + c1
# b2*n <= a2*m + c2
# (b1, b2 > 0)
# return: maximum_or_minimum, m, n_left, n_right
def solve_single_group(a1,b1,c1,a2,b2,c2,has_minimum, minimum, has_maximum, maximum):
    if a1 == 0:
        if a2 == 0:
            l = div_up(c1,b1)
            r = div_down(c2,b2)
            if l > r:
                print("no solution")
                exit()
            return 0, 0, 0, 0
        else:
            l = div_up(c1,b1)
            m_val = b2 * l - c2
            if a2 > 0:
                m_val = div_up(m_val,a2)
                is_maximum = -1
            else:
                m_val = div_down(m_val,a2)
                is_maximum = 1
            r = div_down((a2 * m_val + c2),b2)
            return is_maximum, m_val, l, r
    else:
        if a2 == 0:
            r = div_down(c2,b2)
            m_val = b1 * r - c1
            if a1 > 0:
                m_val = div_down(m_val,a1)
                is_maximum = 1
            else:
                m_val = div_up(m_val,a1)
                is_maximum = -1
            l = div_up((a1 * m_val + c1),b1)
            return is_maximum, m_val, l, r
        else:
            coef = a1 * b2 - a2 * b1
            constant = c1 * b2 - c2 * b1
            if coef == 0:
                if constant > 0:
                    print("no solution")
                    exit()
                return 0, 0, 0, 0
            if a1 > 0 and a2 < 0:
                m_val = div_down(-constant,coef)
                if has_maximum and m_val > maximum:
                    m_val=maximum
                if div_up((a1 * m_val + c1),b1) > div_down((a2 * m_val + c2),b2):
                    n1 = div_up((a1 * m_val + c1),b1) -1
                    n2 = div_down((a2 * m_val + c2),b2) + 1
                    m_val1 = div_down((n1 * b1 - c1),a1)
                    m_val2 = div_down((n2 * b2-c2),a2)
                    if m_val1 > m_val2:
                        m_val=m_val1
                    else:
                        m_val=m_val2
                l = div_up((a1 * m_val + c1),b1)
                r = div_down((a2 * m_val + c2),b2)
                return 1, m_val, l, r
            if a1 < 0 and a2 > 0:
                m_val = div_up(-constant,coef)
                if has_minimum and m_val < minimum:
                    m_val=minimum
                if div_up((a1 * m_val + c1),b1) > div_down((a2 * m_val + c2),b2):
                    n1 = div_up((a1 * m_val + c1),b1) - 1
                    n2 = div_down((a2 * m_val + c2),b2) + 1
                    m_val1 = div_up((n1 * b1 - c1),a1)
                    m_val2 = div_up((n2 * b2-c2),a2)
                    if m_val1 < m_val2:
                        m_val=m_val1
                    else:
                        m_val=m_val2
                l = div_up((a1 * m_val + c1),b1)
                r = div_down((a2 * m_val + c2),b2)
                return -1, m_val, l, r
            l_min = div_up((a1 * minimum + c1),b1)
            r_min = div_down((a2 * minimum + c2),b2)
            l_max = div_up((a1 * maximum + c1),b1)
            r_max = div_down((a2 * maximum + c2),b2)
            r_min2 = div_up((a2 * minimum + c2),b2)
            l_max2 = div_down((a1 * maximum + c1),b1)
            if a1 * b2 > a2 * b1:
                if a1 >= b1 or a1 < 0:
                    q = div_down(a1,b1)
                    is_maximum, m_val, l_, r_ = solve_single_group(a1-q*b1, b1, c1, a2-q*b2, b2, c2, has_minimum, minimum, has_maximum, maximum)
                else:
                    is_maximum = 1
                    if has_maximum:
                        is_maximum_, m_val_, l_, r_ = solve_single_group(b2, a2, -c2, 0, 1, maximum, has_minimum, l_min, has_maximum, r_max)
                        m_val = r_
                    if has_maximum == 0 or m_val_ < l_max:
                        is_maximum_, m_val_, l_, r_ = solve_single_group(b2, a2, -c2, b1, a1, -c1, has_minimum, l_min, has_maximum, l_max2)
                        m_val = r_
            else:
                if a2 >= b2 or a2 < 0:
                    q = div_down(a2,b2)
                    is_maximum, m_val, l_, r_ = solve_single_group(a1-q*b1, b1, c1, a2-q*b2, b2, c2, has_minimum, minimum, has_maximum, maximum)
                else:
                    is_maximum = -1
                    if has_minimum:
                        is_maximum_, m_val_, l_, r_ = solve_single_group(0, 1, minimum, b1, a1, -c1, has_minimum, l_min, has_maximum, r_max)
                        m_val = l_ 
                    if has_minimum == 0 or m_val_ > r_min:
                        is_maximum_, m_val_, l_, r_ = solve_single_group(b2, a2, -c2, b1, a1, -c1, has_minimum, r_min2, has_maximum, r_max)
                        m_val = l_
            l = div_up((a1 * m_val + c1),b1)
            r = div_down((a2 * m_val + c2),b2)
            return is_maximum, m_val, l, r
        
# b1*n >= a1*m + c1
# b2*n <= a2*m + c2
# (b1, b2 > 0)
# return: maximum_or_minimum, m, n_left, n_right
def solve_single_group2(a1,b1,c1,a2,b2,c2,has_minimum, minimum, has_maximum, maximum, func):
    if func == 0 and a1*b2 != a2*b1:
        return 0, 0, 0, 0
    is_maximum_, m_val_, l_, r_ = solve_single_group(a1, b1, c1, a2, b2, c2, 0, 0, 0, 0)
    if is_maximum_ == 1 and has_minimum and m_val_ < minimum:
        print("no solution")
        exit()
    if is_maximum_ == -1 and has_maximum and m_val_ > maximum:
        print("no solution")
        exit()
    if a1 == 0 and a2 == 0:
        n1 = div_up(c1,b1)
        n2 = div_down(c2,b2)
        if n1 > n2:
            print("no solution")
            exit()
        if func:
            if has_minimum:
                return -1, minimum, n1, n2
            else:
                return 0, 0, 0, 0
        else:
            if has_maximum:
                return 1, maximum, n1, n2
            else:
                return 0, 0, 0, 0

    if a1 > 0 and a2 <= 0:
        if has_minimum:
            is_maximum = -1
            is_maximum_, m_val_, l_, r_ = solve_single_group(0, 1, minimum, b1, a1, -c1, 0, 0, 0, 0)
            m_val = l_
            l = div_up((a1 * m_val + c1),b1)
            r = div_down((a2 * m_val + c2),b2)
            return is_maximum, m_val, l, r
        else:
            return 0, 0, 0, 0
    if a1 <= 0 and a2 > 0:
        if has_maximum:
            is_maximum = 1
            is_maximum_, m_val_, l_, r_ = solve_single_group(b2, a2, -c2, 0, 1, maximum, 0, 0, 0, 0)
            m_val = r_
            l = div_up((a1 * m_val + c1),b1)
            r = div_down((a2 * m_val + c2),b2)
            return is_maximum, m_val, l, r
        else:
            return 0, 0, 0, 0
    if a1 < 0 and a2 == 0:
        if has_maximum:
            is_maximum = 1
            is_maximum_, m_val_, l_, r_ = solve_single_group(-b1, -a1, c1, 0, 1, maximum, 0, 0, 0, 0)
            m_val = r_
            l = div_up((a1 * m_val + c1),b1)
            r = div_down((a2 * m_val + c2),b2)
            return is_maximum, m_val, l, r
        else:
            return 0, 0, 0, 0
    if a2 < 0 and a1 == 0:
        if has_minimum:
            is_maximum = -1
            is_maximum_, m_val_, l_, r_ = solve_single_group(0, 1, minimum, -b2, -a2, c2, 0, 0, 0, 0)
            m_val = l_
            l = div_up((a1 * m_val + c1),b1)
            r = div_down((a2 * m_val + c2),b2)
            return is_maximum, m_val, l, r
        else:
            return 0, 0, 0, 0
    l_min = div_up((a1 * minimum + c1),b1)
    r_min = div_down((a2 * minimum + c2),b2)
    l_max = div_up((a1 * maximum + c1),b1)
    r_max = div_down((a2 * maximum + c2),b2)
    r_min2 = div_up((a2 * minimum + c2),b2)
    l_max2 = div_down((a1 * maximum + c1),b1)
    if a1 * b2 == a2 * b1:
        if a1 >= b1 or a1 < 0:
            q = div_down(a1,b1)
            is_maximum, m_val, l_, r_ = solve_single_group2(a1-q*b1, b1, c1, a2-q*b2, b2, c2, has_minimum, minimum, has_maximum, maximum, func)
        else:
            if func:
                if has_minimum:
                    is_maximum = -1
                    is_maximum_, m_val_, l_, r_ = solve_single_group(0, 1, minimum, b1, a1, -c1, has_minimum, l_min, has_maximum, r_max)
                    m_val = l_
                    if m_val_ > r_min:
                        is_maximum_, m_val_, l_, r_ = solve_single_group2(b2, a2, -c2, b1, a1, -c1, has_minimum, r_min2, has_maximum, r_max, func)
                        m_val = l_
                else:
                    return 0, 0, 0, 0
            else:
                if has_maximum:
                    is_maximum = 1
                    is_maximum_, m_val_, l_, r_ = solve_single_group(b2, a2, -c2, 0, 1, maximum, has_minimum, l_min, has_maximum, r_max)
                    m_val = r_
                    if m_val_ < l_max:
                        is_maximum_, m_val_, l_, r_ = solve_single_group2(b2, a2, -c2, b1, a1, -c1, has_minimum, l_min, has_maximum, l_max2, func)
                        m_val = r_
                else:
                    return 0, 0, 0, 0
                
    if a1 * b2 > a2 * b1:
        if has_minimum:
            if a1 >= b1 or a1 < 0:
                q = div_down(a1,b1)
                is_maximum, m_val, l_, r_ = solve_single_group2(a1-q*b1, b1, c1, a2-q*b2, b2, c2, has_minimum, minimum, has_maximum, maximum, func)
            else:
                is_maximum = -1
                is_maximum_, m_val_, l_, r_ = solve_single_group(0, 1, minimum, b1, a1, -c1, has_minimum, l_min, has_maximum, r_max)
                m_val = l_
                if m_val_ > r_min:
                    is_maximum_, m_val_, l_, r_ = solve_single_group2(b2, a2, -c2, b1, a1, -c1, has_minimum, r_min2, has_maximum, r_max, func)
                    m_val = l_
        else:
            return 0, 0, 0, 0
    if a1 * b2 < a2 * b1:
        if has_maximum:
            if a2 >= b2 or a2 < 0:
                q = div_down(a2,b2)
                is_maximum, m_val, l_, r_ = solve_single_group2(a1-q*b1, b1, c1, a2-q*b2, b2, c2, has_minimum, minimum, has_maximum, maximum, func)
            else:
                is_maximum = 1
                is_maximum_, m_val_, l_, r_ = solve_single_group(b2, a2, -c2, 0, 1, maximum, has_minimum, l_min, has_maximum, r_max)
                m_val = r_
                if m_val_ < l_max:
                    is_maximum_, m_val_, l_, r_ = solve_single_group2(b2, a2, -c2, b1, a1, -c1, has_minimum, l_min, has_maximum, l_max2, func)
                    m_val = r_
        else:
            return 0, 0, 0, 0
    l = div_up((a1 * m_val + c1),b1)
    r = div_down((a2 * m_val + c2),b2)
    return is_maximum, m_val, l, r

ineq_count = int(input("input the number of inequalities: "))
if ineq_count <= 0:
    print("input out of range")
    exit()
i = 0
ineq_list=[]
while i < ineq_count:
    a = int(input("input the coefficient a of the inequality "+str(i+1)+" (a*x + b*y >= c): "))
    b = int(input("input the coefficient b of the inequality "+str(i+1)+" (a*x + b*y >= c): "))
    if a == 0 and b == 0:
        print("bad input: a and b are both zero")
        exit()
    c =int(input("input the coefficient c of the inequality "+str(i+1)+" (a*x + b*y >= c): "))
    ineq_list.append([a,b,c])
    i += 1
obj_a = int(input("input the coefficient a of the objective function (z = a*x + b*y): "))
obj_b = int(input("input the coefficient b of the objective function (z = a*x + b*y): "))
if obj_a == 0 and obj_b == 0:
    print("bad input: a and b are both zero")
    exit()
# z = a*(c*x+d*y)+b*(e*x+f*y)
obj_c=1
obj_d=0
obj_e=0
obj_f=1
if obj_a < 0:
    obj_c = -1
    obj_a = -obj_a
    i = 0
    while i < ineq_count:
        ineq_list[i][0] = -ineq_list[i][0]
        i += 1
if obj_b < 0:
    obj_f = -1
    obj_b = -obj_b
    i = 0
    while i < ineq_count:
        ineq_list[i][1] = -ineq_list[i][1]
        i += 1
while obj_a != 0 and obj_b != 0:
    q = obj_b // obj_a
    obj_b -= q * obj_a
    obj_c += q * obj_e
    obj_d += q * obj_f
    i = 0
    while i < ineq_count:
        ineq_list[i][1] -= q * ineq_list[i][0]
        i += 1
    if obj_b != 0:
        q = obj_a // obj_b
        obj_a -= q * obj_b
        obj_e += q * obj_c
        obj_f += q * obj_d
        i = 0
        while i < ineq_count:
            ineq_list[i][0] -= q * ineq_list[i][1]
            i += 1
if obj_a == 0:
    obj_a = obj_b
    obj_c, obj_e = obj_e, obj_c
    obj_d, obj_f = obj_f, obj_d
    i = 0
    while i < ineq_count:
        ineq_list[i][0], ineq_list[i][1] = ineq_list[i][1], ineq_list[i][0]
        i += 1

minimum_n_valid = 0
maximum_n_valid = 0
s = 1
while s != 0:
    s = 0
    i = 0
    while i < ineq_count:
        if ineq_list[i][1] == 0:
            if ineq_list[i][0] == 0:
                if ineq_list[i][2] > 0:
                    print("no solution")
                    exit()
            else:
                if ineq_list[i][0] > 0:
                    value = div_up(ineq_list[i][2],ineq_list[i][0])
                    if has_minimum == 0 or minimum < value:
                        s = 1
                        has_minimum = 1
                        minimum_n_valid = 0
                        minimum = value
                else:
                    value = div_down(ineq_list[i][2],ineq_list[i][0])
                    if has_maximum == 0 or maximum > value:
                        s = 1
                        has_maximum = 1
                        maximum_n_valid = 0
                        maximum = value
        else:
            j = i + 1
            while j < ineq_count:
                is_maximum = 0
                if ineq_list[i][1] > 0 and ineq_list[j][1] < 0:
                    is_maximum, value, l, r = solve_single_group(-ineq_list[i][0],ineq_list[i][1],ineq_list[i][2],ineq_list[j][0],-ineq_list[j][1],-ineq_list[j][2], has_minimum, minimum, has_maximum, maximum)
                if ineq_list[i][1] < 0 and ineq_list[j][1] > 0:
                    is_maximum, value, l, r = solve_single_group(-ineq_list[j][0],ineq_list[j][1],ineq_list[j][2],ineq_list[i][0],-ineq_list[i][1],-ineq_list[i][2], has_minimum, minimum, has_maximum, maximum)
                if is_maximum == 1:
                    if has_maximum == 0 or maximum > value or (maximum == value and (maximum_n_valid == 0 or maximum_n < l)):
                        s = 1
                        has_maximum = 1
                        maximum = value
                        maximum_n_valid = 1
                        maximum_n = l
                if is_maximum == -1:
                    if has_minimum == 0 or minimum < value or (minimum == value and (minimum_n_valid == 0 or minimum_n < l)):
                        s = 1
                        has_minimum = 1
                        minimum = value
                        minimum_n_valid = 1
                        minimum_n = l
                j += 1
            j = i + 1
            while j < ineq_count:
                if ineq_list[i][1] > 0 and ineq_list[j][1] < 0:
                    is_maximum, value, l, r = solve_single_group2(-ineq_list[i][0],ineq_list[i][1],ineq_list[i][2],ineq_list[j][0],-ineq_list[j][1],-ineq_list[j][2], has_minimum, minimum, has_maximum, maximum, 1)
                if ineq_list[i][1] < 0 and ineq_list[j][1] > 0:
                    is_maximum, value, l, r = solve_single_group2(-ineq_list[j][0],ineq_list[j][1],ineq_list[j][2],ineq_list[i][0],-ineq_list[i][1],-ineq_list[i][2], has_minimum, minimum, has_maximum, maximum, 1)
                if is_maximum == 1:
                    if has_maximum == 0 or maximum > value or (maximum == value and (maximum_n_valid == 0 or maximum_n < l)):
                        s = 1
                        has_maximum = 1
                        maximum = value
                        maximum_n_valid = 1
                        maximum_n = l
                if is_maximum == -1:
                    if has_minimum == 0 or minimum < value or (minimum == value and (minimum_n_valid == 0 or minimum_n < l)):
                        s = 1
                        has_minimum = 1
                        minimum = value
                        minimum_n_valid = 1
                        minimum_n = l
                j += 1
            j = i + 1
            while j < ineq_count:
                if ineq_list[i][1] > 0 and ineq_list[j][1] < 0:
                    is_maximum, value, l, r = solve_single_group2(-ineq_list[i][0],ineq_list[i][1],ineq_list[i][2],ineq_list[j][0],-ineq_list[j][1],-ineq_list[j][2], has_minimum, minimum, has_maximum, maximum, 0)
                if ineq_list[i][1] < 0 and ineq_list[j][1] > 0:
                    is_maximum, value, l, r = solve_single_group2(-ineq_list[j][0],ineq_list[j][1],ineq_list[j][2],ineq_list[i][0],-ineq_list[i][1],-ineq_list[i][2], has_minimum, minimum, has_maximum, maximum, 0)
                if is_maximum == 1:
                    if has_maximum == 0 or maximum > value or (maximum == value and (maximum_n_valid == 0 or maximum_n < l)):
                        s = 1
                        has_maximum = 1
                        maximum = value
                        maximum_n_valid = 1
                        maximum_n = l
                if is_maximum == -1:
                    if has_minimum == 0 or minimum < value or (minimum == value and (minimum_n_valid == 0 or minimum_n < l)):
                        s = 1
                        has_minimum = 1
                        minimum = value
                        minimum_n_valid = 1
                        minimum_n = l
                j += 1
        i += 1
    if has_maximum and has_minimum and minimum > maximum:
        print("no solution")
        exit()
if has_maximum and maximum_n_valid == 0:
    i = 0
    is_maximum = 0
    maximum_n = 0
    while i < ineq_count:
        value = maximum * ineq_list[i][0] - ineq_list[i][2]
        if ineq_list[i][1] > 0:
            value = div_up(-value,ineq_list[i][1])
            if is_maximum <= 0:
                if is_maximum == 0 or maximum_n < value:
                    maximum_n = value
                is_maximum = -1
        if ineq_list[i][1] < 0:
            value = div_down(-value,ineq_list[i][1])
            if is_maximum >= 0:
                if is_maximum == 0 or maximum_n > value:
                    maximum_n = value
                is_maximum = 1
        i += 1
if has_minimum and minimum_n_valid == 0:
    i = 0
    is_maximum = 0
    minimum_n = 0
    while i < ineq_count:
        value = minimum * ineq_list[i][0] - ineq_list[i][2]
        if ineq_list[i][1] > 0 and is_maximum <= 0:
            value = div_up(-value,ineq_list[i][1])
            if is_maximum <= 0:
                if is_maximum == 0 or minimum_n < value:
                    minimum_n = value
                is_maximum = -1
        if ineq_list[i][1] < 0 and is_maximum >= 0:
            value = div_down(-value,ineq_list[i][1])
            if is_maximum >= 0:
                if is_maximum == 0 or minimum_n > value:
                    minimum_n = value
                is_maximum = 1
        i += 1
if has_maximum:
    x_val = (maximum * obj_f - maximum_n * obj_d) // (obj_c * obj_f - obj_d * obj_e)
    y_val = (maximum_n * obj_c - maximum * obj_e) // (obj_c * obj_f - obj_d * obj_e)
    maximum *= obj_a
    print("z_max = "+str(maximum)+" at x = "+str(x_val)+", y = "+str(y_val))
else:
    print("no maximum")
if has_minimum:
    x_val = (minimum * obj_f - minimum_n * obj_d) // (obj_c * obj_f - obj_d * obj_e)
    y_val = (minimum_n * obj_c - minimum * obj_e) // (obj_c * obj_f - obj_d * obj_e)
    minimum *= obj_a
    print("z_min = "+str(minimum)+" at x = "+str(x_val)+", y = "+str(y_val))
else:
    print("no minimum")
