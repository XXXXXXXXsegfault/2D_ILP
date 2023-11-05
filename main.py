def no_solution():
    print("no solution")
    exit()

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
has_minimum=0
has_maximum=0
minimum=0
maximum=0
def set_minimum(value):
    global minimum, has_minimum, maximum, has_maximum
    if has_minimum == 0 or value > minimum:
        has_minimum = 1
        minimum = value
        if has_minimum and has_maximum and minimum > maximum:
            no_solution()
def set_maximum(value):
    global minimum, has_minimum, maximum, has_maximum
    if has_maximum == 0 or value < maximum:
        has_maximum = 1
        maximum = value
        if has_minimum and has_maximum and minimum > maximum:
            no_solution()

# b1*n >= a1*m + c1
# b2*n <= a2*m + c2
# b1, b2 are positive integers
# return: new_value, l, r
def update_minimum(a1,b1,c1,a2,b2,c2,value):
    l = div_up(a1 * value + c1,b1)
    r = div_down(a2 * value + c2,b2)
    if l <= r:
        return value, l, r
    if a1 >= 0 and a2 <= 0:
        no_solution()
    if a1 <= 0 and a2 >= 0:
        val1 = div_up(div_down(a1 * value + c1,b1) * b1 - c1,a1)
        val2 = div_up(div_up(a2 * value + c2,b2) * b2 - c2,a2)
        new_value = min(val1,val2)
        l = div_up(a1 * new_value + c1,b1)
        r = div_down(a2 * new_value + c2,b2)
        return new_value, l, r
    if a1 * b2 > a2 * b1:
        if a1 < 0 or a1 >= b1:
            q = div_down(a1,b1)
            new_value, l1, r1 = update_minimum(a1-q*b1,b1,c1,a2-q*b2,b2,c2, value)
            l = div_up(a1 * new_value + c1,b1)
            r = div_down(a2 * new_value + c2,b2)
            return new_value, l, r
    else:
        if a2 < 0 or a2 >= b2:
            q = div_down(a2,b2)
            new_value, l1, r1 = update_minimum(a1-q*b1,b1,c1,a2-q*b2,b2,c2, value)
            l = div_up(a1 * new_value + c1,b1)
            r = div_down(a2 * new_value + c2,b2)
            return new_value, l, r
    val1, new_value, r1 = update_minimum(b2, a2, -c2, b1, a1, -c1, div_up(a2 * value + c2, b2))
    l = div_up(a1 * new_value + c1,b1)
    r = div_down(a2 * new_value + c2,b2)
    return new_value, l, r

def update_maximum(a1,b1,c1,a2,b2,c2,value):
    new_value, l1, r1 = update_minimum(-a1, b1, c1, -a2, b2, c2, -value)
    new_value = -new_value
    l = div_up(a1 * new_value + c1,b1)
    r = div_down(a2 * new_value + c2,b2)
    return new_value, l, r

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

# solve the problem without integer restrictions
i = 0
while i < ineq_count:
    if ineq_list[i][1] == 0:
        if ineq_list[i][0] == 0:
            if ineq_list[i][2] > 0:
                no_solution()
        else:
            if ineq_list[i][0] > 0:
                set_minimum(div_up(ineq_list[i][2],ineq_list[i][0]))
            else:
                set_maximum(div_down(ineq_list[i][2],ineq_list[i][0]))
    else:
        j = 0
        while j < ineq_count:
            if ineq_list[i][1] > 0 and ineq_list[j][1] < 0:
                a=ineq_list[i][0] * ineq_list[j][1] - ineq_list[j][0] * ineq_list[i][1]
                c=ineq_list[i][2] * ineq_list[j][1] - ineq_list[j][2] * ineq_list[i][1]
                if a == 0:
                    if c > 0:
                        no_solution()
                else:
                    if a > 0:
                        set_maximum(div_down(c,a))
                    else:
                        set_minimum(div_up(c,a))
            j += 1
    i += 1
# take integer restrictions into consideration
status = 1
while status == 1:
    status = 0
    i = 0
    while i < ineq_count:
        j = 0
        while j < ineq_count:
            if ineq_list[i][1] > 0 and ineq_list[j][1] < 0:
                if has_minimum != 0:
                    value, l, r = update_minimum(-ineq_list[i][0],ineq_list[i][1],ineq_list[i][2],ineq_list[j][0],-ineq_list[j][1],-ineq_list[j][2],minimum)
                    if value != minimum:
                        status = 1
                    set_minimum(value)
                if has_maximum != 0:
                    value, l, r = update_maximum(-ineq_list[i][0],ineq_list[i][1],ineq_list[i][2],ineq_list[j][0],-ineq_list[j][1],-ineq_list[j][2],maximum)
                    if value != maximum:
                        status = 1
                    set_maximum(value)
            j += 1
        i += 1

if has_maximum:
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
if has_minimum:
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

