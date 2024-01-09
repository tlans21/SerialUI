shift_n = 0x01

target_16bit = 0xa1d2
print(type(target_16bit))
print(bin(0xa1d2)[2:])
value_list = []
for i in range(0, 16):
    #1010000111010010 

    value = bin(target_16bit & shift_n)[2:]
    value_list.append(value)
    shift_n = (0x01 << (i+1))

print(value_list)