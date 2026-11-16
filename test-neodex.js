// lancé par le test « local » de NeoDex : le thème Ado se choisit, son décor (ado.css) arrive dans la page sans rien qui vienne d'Internet,
// puis repart quand on change de thème ; captures de l'accueil et de la galerie des thèmes
module.exports = async ({ js, sleep, shot = async () => {} }) => {
  const k = 'plugin:neodex.themeado:ado';
  if (!await js(`!!THEMES['${k}']`)) throw new Error('le thème Ado n’est pas dans la liste');
  await js(`(applyTheme('${k}'), 0)`); await sleep(1200); await js(`document.fonts.load('20px "Rampart One"').then(() => 0)`);
  const r = await js(`(() => { const st = document.getElementById('plugThemeCss'), css = st?.textContent || '';
    return { style: document.documentElement.dataset.style, len: css.length, deco: css.includes('GYARU'), font: document.fonts.check('20px "Rampart One"'), sign: getComputedStyle(document.querySelector('.panel'), '::after').backgroundImage.slice(0, 30), walk: getComputedStyle(document.documentElement, '::before').animationName, net: /url\\(\\s*(?!['"]?data:)/i.test(css), magenta: getComputedStyle(document.documentElement).getPropertyValue('--magenta').trim(),
      before: getComputedStyle(document.body, '::before').backgroundImage.slice(0, 30), bar: typeof plugThemeBarCss === 'string' && plugThemeBarCss.includes('#start') }; })()`);
  if (r.style !== 'cyber' || !r.deco || !r.font || !/^url\("data:image\/png/.test(r.sign) || !/adoWalk/.test(r.walk) || r.net || !/url\("data/.test(r.before) || !r.bar) throw new Error('décor : ' + JSON.stringify(r));
  await shot('accueil');
  await js(`(document.querySelector('.hTitle')?.scrollIntoView(), 0)`);
  await js(`(applyTheme('nebula'), 0)`); await sleep(500);
  const gone = await js(`!document.getElementById('plugThemeCss')`);
  if (!gone) throw new Error('le décor reste après un changement de thème');
  await js(`(applyTheme('${k}'), $('bSettings').click(), 0)`); await sleep(1500);
  await js(`([...document.querySelectorAll('#setModal *')].find(x => x.children.length === 0 && x.textContent.trim() === 'Apparence')?.click(), 0)`); await sleep(600);
  await shot('galerie');
  await js(`($('setClose')?.click(), 0)`);
  return `style ${r.style} · accent ${r.magenta} · police Rampart One chargée · Abo sur les cadres et en promenade · barre des tâches stylée · décor de ${r.len} caractères, rien d'Internet · retiré au changement de thème`;
};
