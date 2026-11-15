import { readFileSync, statSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const root = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(resolve(root, 'dist/app.js'), 'utf8');
const dataOnly = source.slice(0, source.indexOf('const state='));
const context = vm.createContext({});
vm.runInContext(dataOnly + '\nthis.exerciseData={easy,medium,advanced3,advanced4,board,books};', context);
const { easy, medium, advanced3, advanced4, board, books } = context.exerciseData;

function checkExercises(items, label) {
  assert.equal(items.length, 12, `${label} heeft 12 opdrachten`);
  for (const [i, task] of items.entries()) {
    assert.ok(task.title && task.prompt && task.hint, `${label} ${i + 1} is volledig`);
    assert.ok(['choice', 'story', 'open'].includes(task.kind));
    if (task.kind === 'open') {
      assert.ok(task.words?.length >= 3);
    } else {
      assert.ok(task.options?.length >= 2);
      assert.ok(Number.isInteger(task.answer));
      assert.ok(task.answer >= 0 && task.answer < task.options.length);
      assert.equal(new Set(task.options).size, task.options.length, 'geen dubbele keuzen');
      if (task.kind === 'story') assert.ok(task.story?.length >= 30);
    }
  }
  console.log(`OK ${label}: ${items.length} complete opdrachten`);
}

checkExercises(easy, 'Niveau 1');
checkExercises(medium, 'Niveau 2');
checkExercises(advanced3, 'Niveau 3');
checkExercises(advanced4, 'Niveau 4');
assert.equal(Object.keys(books).length, 4, 'vier niveaus beschikbaar');
for (const [name, items] of [['Niveau 3',advanced3],['Niveau 4',advanced4]]) {
  for (const task of items) {
    assert.ok(task.story?.length >= 180, `${name}: elke opdracht heeft een langere tekst`);
    if (task.kind === 'open') assert.ok(task.sample?.length >= 30, `${name}: open opdracht heeft een voorbeeld`);
  }
}
assert.equal(board.length, 7, 'zeven vooraf ingevulde communicatieonderwerpen');
for (const group of board) {
  assert.equal(group.items.length, 9, `communicatieonderwerp ${group.label}`);
  assert.equal(new Set(group.items.map(x => x[1])).size, 9, 'geen dubbele zinnen');
  for (const pair of group.items) assert.ok(pair[0] && pair[1]);
}
console.log(`OK communicatiebord: ${board.length} onderwerpen, 63 zinnen`);

const html = readFileSync(resolve(root, 'dist/index.html'), 'utf8');
for (const id of ['homeBtn','main','resetBtn','contrastBtn','biggerText','smallerText','toast']) {
  assert.ok(html.includes(`id="${id}"`), `benodigd element ${id}`);
}
const css = readFileSync(resolve(root, 'dist/style.css'), 'utf8');
assert.ok(css.includes('@media(max-width:650px)'), 'telefoon-schermopmaak aanwezig');
assert.ok(css.includes('@media(max-width:900px)'), 'tablet-schermopmaak aanwezig');
assert.ok(source.includes('const state={view:"choose"'), 'niveaukeuze verschijnt bij openen');
const levelPage=source.slice(source.indexOf('function choosePage()'),source.indexOf('function homePage()'));
for (const choice of ['easy','medium','advanced','expert','board']) {
  assert.ok(levelPage.includes(`data-action="${choice}"`), `${choice} staat in het beginscherm`);
}
assert.ok(levelPage.includes('data-action="info"'), 'uitleg en downloads blijven bereikbaar');
assert.ok(source.includes('if(action==="info")return showInfo()'), 'navigatie naar uitleg werkt');
assert.ok(css.includes('.level-start') && css.includes('.level-grid'), 'niveaukeuze is opgemaakt');
console.log('OK website: knoppen, schermgroottes en navigatie aanwezig');

for (const name of ['01-woorden-terugvinden','02-zinnen-en-verhalen','03-ik-wil-iets-vertellen','niveau-3-teksten-begrijpen','niveau-4-denken-en-verwoorden']) {
  const file=resolve(root,`dist/pdf/${name}.pdf`);
  assert.ok(statSync(file).size > 20000, `${name} is geen leeg bestand`);
  assert.equal(readFileSync(file).subarray(0,4).toString(),'%PDF');
  assert.ok(source.includes(`pdf/${name}.pdf`), `${name} heeft een downloadlink`);
}
console.log('OK downloads: alle 5 PDF-boekjes gekoppeld');
console.log('Alle geautomatiseerde controlepunten geslaagd.');
