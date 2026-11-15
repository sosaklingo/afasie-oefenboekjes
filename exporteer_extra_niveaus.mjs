#!/usr/bin/env node
// Genereert gegevens voor de printbare boekjes uit de bron van de website.
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const dir = dirname(fileURLToPath(import.meta.url));
const sourceFile = resolve(process.argv[2] || resolve(dir, 'website/dist/app.js'));
const targetFile = resolve(process.argv[3] || resolve(dir, 'levels-extra.json'));
const source = readFileSync(sourceFile, 'utf8');
const marker = source.indexOf('const state=');
if (marker < 0) throw Error('Kan oefengegevens niet vinden in de website');
const context = vm.createContext({});
vm.runInContext(source.slice(0, marker) + '\nthis.exportData={advanced3,advanced4};', context, {timeout: 5000});
const data = JSON.parse(JSON.stringify(context.exportData));
if (data.advanced3.length !== 12 || data.advanced4.length !== 12) {
  throw Error('Elk nieuw niveau moet 12 opdrachten bevatten');
}
writeFileSync(targetFile, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log(`24 opdrachten geëxporteerd naar ${targetFile}`);
