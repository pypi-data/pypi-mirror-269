d, ra, rall = '[0m', '[0m', '[0m' # Delete/Reset ALL transformation

### Transformation
# `t*` : to -> permit to apply the transformation
# `r*` : reset -> permit to remove the transformation
ti0, ti1, ti2 = '[2m', '[22m', '[1m' # Intensity (week, normal, strong)
ti, ri = '[3m', '[23m' # Italic
tu, ru = '[4m', '[24m' # Underline
tu2, ru2 = '[21m', '[24m' # Double Underline
tb, rb = '[5m', '[25m' # Blink
tr, rr = '[7m', '[27m' # Reset
th, rh = '[8m', '[28m' # Hide
tc, rc = '[9m', '[29m' # Cross

### Font Color (`l` for light) :
k, lk = '[30m', '[90m' # Black
r, lr = '[31m', '[91m' # Red
g, lg = '[32m', '[92m' # Green
y, ly = '[33m', '[93m' # Yellow
b, lb = '[34m', '[94m' # Blue
m, lm = '[35m', '[95m' # Magenta
c, lc = '[36m', '[96m' # Cyan
w, lw = '[37m', '[97m' # White
rfc = '[39m' # Reset font color

### Back Color (`l` for light) :
bk, blk = '[40m', '[100m' # Black
br, blr = '[41m', '[101m' # Red
bg, blg = '[42m', '[102m' # Green
by, bly = '[43m', '[103m' # Yellow
bb, blb = '[44m', '[104m' # Blue
bm, blm = '[45m', '[105m' # Magenta
bc, blc = '[46m', '[106m' # Cyan
bw, blw = '[47m', '[107m' # White
rbc = '[49m' # Reset back color

# Dict of ansi codes : 
ansi = {
	'd' : 0,
	'ra' : 0,
	'rall' : 0,
	'ti0' : 2,
	'ti1' : 22,
	'ti2' : 1,
	'ti' : 3,
	'ri' : 23,
	'tu' : 4,
	'ru' : 24,
	'tu2' : 21,
	'ru2' : 24,
	'tb' : 5,
	'rb' : 25,
	'tr' : 7,
	'rr' : 27,
	'th' : 8,
	'rh' : 28,
	'tc' : 9,
	'rc' : 29,
	'k' : 30,
	'lk' : 90,
	'r' : 31,
	'lr' : 91,
	'g' : 32,
	'lg' : 92,
	'y' : 33,
	'ly' : 93,
	'b' : 34,
	'lb' : 94,
	'm' : 35,
	'lm' : 95,
	'c' : 36,
	'lc' : 96,
	'w' : 37,
	'lw' : 97,
	'rfc' : 39,
	'bk' : 40,
	'blk' : 100,
	'br' : 41,
	'blr' : 101,
	'bg' : 42,
	'blg' : 102,
	'by' : 43,
	'bly' : 103,
	'bb' : 44,
	'blb' : 104,
	'bm' : 45,
	'blm' : 105,
	'bc' : 46,
	'blc' : 106,
	'bw' : 47,
	'blw' : 107,
	'rbc' : 49,
}