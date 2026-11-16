# Prépare les images du thème Ado à partir des images d'origine (dossier donné en argument, pas dans le dépôt) :
#   2.jpg  la peluche « Abo » (le mème « I am Ado ») -> img/abo.png détourée, sans la bulle, bordure noire d'autocollant
#   3.jpg  la rose bleue sur fond noir                -> img/rose-hg/hd/bg/bd.png détourée (son contour noir gardé), une par coin, tournée vers le milieu
#   4.jpg  l'illustration                             -> img/fond.jpg
# python tools/images.py <dossier des images>   (depuis le dossier du plugin)
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd

src = sys.argv[1]; os.makedirs('img', exist_ok=True)

def save_rgba(rgb, mask, path, feather=1.2):
    a = Image.fromarray((mask * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(feather))
    im = Image.fromarray(rgb).convert('RGBA'); im.putalpha(a); im = im.crop(im.getbbox()); im.save(path, optimize=True); return im

# la peluche : agrandie 4 fois avant la découpe (l'image d'origine fait 140 px) ; le fond blanc touche les bords, on garde la tache
# qui contient son ventre (la bulle est à part), trous bouchés (gants, chemise), contour lissé, puis le blanc du fond retiré des bords
P = Image.open(os.path.join(src, '2.jpg')).convert('RGB'); P = P.resize((P.width * 4, P.height * 4), Image.LANCZOS).filter(ImageFilter.SMOOTH)
p = np.asarray(P).astype(float)
white = (p.min(2) > 214) & (p.max(2) - p.min(2) < 30)
lab, _ = nd.label(white); bg = np.isin(lab, np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) & white
obj, _ = nd.label(~bg); h, w = obj.shape
body = obj == obj[int(h * .78), w // 2]
body = nd.binary_fill_holes(nd.binary_opening(nd.binary_closing(body, iterations=3), iterations=3))
ys = np.arange(h)[:, None] > h * .74; body &= ~(white & ys)      # en bas, le blanc coincé entre les mèches et les jambes est du fond (la chemise s'arrête plus haut)
body = nd.binary_opening(body, iterations=2)
lab2, _ = nd.label(body); body = lab2 == lab2[int(h * .55), w // 2]
body = nd.binary_fill_holes(body); body &= ~(white & (np.arange(h)[:, None] > h * .84))   # chemise et gants rebouchés, les poches du bas restent vides
soft = nd.gaussian_filter(body.astype(float), 3.5); body = soft > .55          # contour lissé (fini les marches du JPEG)
a = np.clip(nd.gaussian_filter(nd.binary_erosion(body, iterations=3).astype(float), 1.1) * 1.15 - .08, 0, 1)  # rogné : le bord clair du JPEG passe sous la bordure noire    # bord doux sur 2 à 3 points
k = a[..., None]; rgb = np.where(k > .02, (p - (1 - k) * 255) / np.maximum(k, .02), p)  # ôte le blanc mêlé aux bords
rgb = np.clip(rgb, 0, 255).astype('uint8')
im = Image.fromarray(rgb).convert('RGBA'); im.putalpha(Image.fromarray((a * 255).astype('uint8')))
# une bordure noire tout autour, comme un autocollant (à la place du liseré blanc)
ring = np.clip(nd.gaussian_filter(nd.binary_dilation(body, iterations=6).astype(float), 1.5) * 1.1, 0, 1)
out = Image.new('RGBA', im.size, (2, 6, 21, 0)); out.putalpha(Image.fromarray((ring * 255).astype('uint8'))); out.alpha_composite(im); im = out.crop(out.getbbox())
im.thumbnail((150, 190), Image.LANCZOS); im.save('img/abo.png', optimize=True)

# la rose : le bleu, ses trous bouchés, puis élargi pour reprendre le trait noir du contour
r = np.asarray(Image.open(os.path.join(src, '3.jpg')).convert('RGB')).astype(int)
blue = (r[..., 2] - r[..., 0] > 28) & (r[..., 2] > 60)
m = nd.binary_fill_holes(nd.binary_closing(blue, iterations=4))
m = nd.binary_dilation(m, iterations=7)
im = save_rgba(r.astype('uint8'), m, 'img/rose.png', 1.5)
im.thumbnail((280, 280), Image.LANCZOS); q = im.quantize(64, method=Image.Quantize.FASTOCTREE); q.save('img/rose.png', optimize=True)  # dessin en aplats : 64 couleurs suffisent
os.remove('img/rose.png')
# une rose par coin, tournée pour que son sommet pointe vers le milieu de l'écran (en haut à droite, elle pointe vers le bas à gauche…)
for corner, angle, flip in (('hg', -135, False), ('hd', 135, True), ('bg', -45, True), ('bd', 45, False)):
    c = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
    c = c.rotate(angle, resample=Image.BICUBIC, expand=True); c = c.crop(c.getbbox())
    c.quantize(64, method=Image.Quantize.FASTOCTREE).save(f'img/rose-{corner}.png', optimize=True)

# le fond : gardé tel quel, juste compressé
Image.open(os.path.join(src, '4.jpg')).convert('RGB').save('img/fond.jpg', quality=84, optimize=True, progressive=True)
for f in ('abo.png', 'rose-hg.png', 'rose-hd.png', 'rose-bg.png', 'rose-bd.png', 'fond.jpg'): print(f, os.path.getsize('img/' + f), 'octets', Image.open('img/' + f).size)
