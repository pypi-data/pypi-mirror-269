
### Transformation
# `t*` : to -> permit to apply the transformation
# Intensity (week, normal, strong)
fti0 = lambda s : print(f"[2m{s}[0m")
fti1 = lambda s : print(f"[22m{s}[0m")
fti2 = lambda s : print(f"[1m{s}[0m")
# Italic
fti = lambda s : print(f"[3m{s}[0m")
# Underline
ftu = lambda s : print(f"[4m{s}[0m")
# Double Underline
ftu2 = lambda s : print(f"[21m{s}[0m")
# Blink
ftb = lambda s : print(f"[5m{s}[0m")
# Hide
fth = lambda s : print(f"[8m{s}[0m")
# Cross
ftc = lambda s : print(f"[9m{s}[0m")

### Font Color (`l` for light) :
# Black
fk = lambda s : print(f"[30m{s}[0m")
flk = lambda s : print(f"[90m{s}[0m")
# Red
fr = lambda s : print(f"[31m{s}[0m")
flr = lambda s : print(f"[91m{s}[0m")
# Green
fg = lambda s : print(f"[32m{s}[0m")
flg = lambda s : print(f"[92m{s}[0m")
# Yellow
fy = lambda s : print(f"[33m{s}[0m")
fly = lambda s : print(f"[93m{s}[0m")
# Blue
fb = lambda s : print(f"[34m{s}[0m")
flb = lambda s : print(f"[94m{s}[0m")
# Magenta
fm = lambda s : print(f"[35m{s}[0m")
flm = lambda s : print(f"[95m{s}[0m")
# Cyan
fc = lambda s : print(f"[36m{s}[0m")
flc = lambda s : print(f"[96m{s}[0m")
# White
fw = lambda s : print(f"[37m{s}[0m")
flw = lambda s : print(f"[97m{s}[0m")

### Back Color (`l` for light) :
# Black
fbk = lambda s : print(f"[40m{s}[0m")
fblk = lambda s : print(f"[100m{s}[0m")
# Red
fbr = lambda s : print(f"[41m{s}[0m")
fblr = lambda s : print(f"[101m{s}[0m")
# Green
fbg = lambda s : print(f"[42m{s}[0m")
fblg = lambda s : print(f"[102m{s}[0m")
# Yellow
fby = lambda s : print(f"[43m{s}[0m")
fbly = lambda s : print(f"[103m{s}[0m")
# Blue
fbb = lambda s : print(f"[44m{s}[0m")
fblb = lambda s : print(f"[104m{s}[0m")
# Magenta
fbm = lambda s : print(f"[45m{s}[0m")
fblm = lambda s : print(f"[105m{s}[0m")
# Cyan
fbc = lambda s : print(f"[46m{s}[0m")
fblc = lambda s : print(f"[106m{s}[0m")
# White
fbw = lambda s : print(f"[47m{s}[0m")
fblw = lambda s : print(f"[107m{s}[0m")
