# __init__.py
from .loc import *
from .func import *


def toCode(c, csi='\033['):
	"""
	Function for encode the transformation number `c`
	Param :
		- c [int or str] : ANSI code
	"""
	return f"{csi}{c}m"

def f(s, args):
	"""
	Function for transform the sentence `s` with transformations containt in `args`
	Param :
		- s [str]    : sentence to tranform
		- args [str] : all code wanted, separated with '.'

	Ex : 
		# For print 'Incroyable Test' underlined (tu), red (r), blink (tb), with green back :
		f('Incroyable Test', 'tu.r.tb.bg')
	"""
	full = ''.join([toCode(ansi[arg]) for arg in args.split('.')])
	print(f"{full}{s}{toCode(0)}")

def test():
	"""
	Function to test the coloralf package. No param.
	"""
	print(f"\nTest of coloralf :")

	print(f"\nTransformations : ")
	fti0('Week intensity   (ti0)')
	fti1('Normal intensity (ti1)')
	fti2('Strong intensity (ti2)')
	fti( 'Italic           (ti)')
	ftu( 'Underline        (tu)')
	ftu2('Double underline (tu2)')
	ftb( 'Blink            (tb)')
	print(f"{th}Hide{rh} (it's hide) (th)")
	ftc( 'Cross            (tc)')

	print("\nChange font color :")
	print(f"{k}Black   (k) {d}-{lk} Light Black   (lk){d}")
	print(f"{r}Red     (r) {d}-{lr} Light Red     (lr){d}")
	print(f"{g}Green   (g) {d}-{lg} Light Green   (lg){d}")
	print(f"{y}Yellow  (y) {d}-{ly} Light Yellow  (ly){d}")
	print(f"{b}Blue    (b) {d}-{lb} Light Blue    (lb){d}")
	print(f"{m}Magenta (k) {d}-{lm} Light Magenta (lm){d}")
	print(f"{c}Cyan    (k) {d}-{lc} Light Cyan    (lc){d}")
	print(f"{w}White   (k) {d}-{lw} Light White   (lw){d}")

	print("\nChange back color :")
	print(f"{bk}Black   (bk) {d}-{blk} Light Black   (blk){d}")
	print(f"{br}Red     (br) {d}-{blr} Light Red     (blr){d}")
	print(f"{bg}Green   (bg) {d}-{blg} Light Green   (blg){d}")
	print(f"{by}Yellow  (by) {d}-{bly} Light Yellow  (bly){d}")
	print(f"{bb}Blue    (bb) {d}-{blb} Light Blue    (blb){d}")
	print(f"{bm}Magenta (bk) {d}-{blm} Light Magenta (blm){d}")
	print(f"{bc}Cyan    (bk) {d}-{blc} Light Cyan    (blc){d}")
	print(f"{bw}White   (bk) {d}-{blw} Light White   (blw){d}")