// The tested site and the GitHub Pages publication must stay byte-for-byte identical.
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repository = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = join(repository, 'website', 'dist');
const published = join(repository, 'docs');

function filesUnder(directory, prefix = '') {
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const name = join(prefix, entry.name);
    const absolute = join(directory, entry.name);
    if (entry.isDirectory()) return filesUnder(absolute, name);
    assert.ok(entry.isFile(), 'Unexpected non-file in website: ' + name);
    return [name];
  }).sort();
}

const sourceFiles = filesUnder(source);
const publishedFiles = filesUnder(published);
assert.deepEqual(
  publishedFiles, sourceFiles,
  'The published docs folder and tested website/dist folder contain different files'
);
for (const file of sourceFiles) {
  assert.ok(
    readFileSync(join(source, file)).equals(readFileSync(join(published, file))),
    'GitHub Pages has different content for: ' + relative(repository, join(published, file))
  );
}
console.log('OK GitHub Pages: ' + sourceFiles.length + ' files are identical to the tested website');
