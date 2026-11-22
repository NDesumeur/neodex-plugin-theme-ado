# Ado theme for NeoDex

A blue and black theme in tribute to Ado: her artwork in the background, blue roses in the corners with sparkling gyaru stickers, Abo (the plush from the "I am Ado" meme) sitting on the edge of each panel and strolling along the taskbar, a scrolling list of her songs at the bottom and a bold, readable NeoDex title, also on the taskbar. A fan theme, not officially linked to the artist.

Install it from NeoStore, Themes category (NeoDex 3.2.2 and later), then pick it in Settings > Appearance. Everything is inside `ado.css`: nothing comes from the internet.

## Credits

- Font: Rampart One by Fontworks, under the SIL Open Font License 1.1 (`fonts/RampartOne.woff2`, reduced to Latin letters).
- The background artwork, the rose and the Abo plush belong to their authors. This fan theme is not officially linked to Ado.

## Rebuilding the decor

`tools/images.py <folder of the original images>` prepares the images in `img`, then `tools/decor.py` puts the font and the decor into `ado.css`.
