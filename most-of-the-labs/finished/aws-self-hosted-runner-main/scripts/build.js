'use strict';

const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..');
const distDir = path.join(root, 'dist');
const srcDir = path.join(root, 'src');

fs.rmSync(distDir, { recursive: true, force: true });

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    entry.isDirectory() ? copyDir(srcPath, destPath) : fs.copyFileSync(srcPath, destPath);
  }
}

copyDir(srcDir, path.join(distDir, 'src'));

const pkg = require('../package.json');
const manifest = {
  name: pkg.name,
  version: pkg.version,
  builtAt: new Date().toISOString(),
  node: process.version,
  files: fs.readdirSync(path.join(distDir, 'src')),
};

fs.writeFileSync(path.join(distDir, 'build-manifest.json'), JSON.stringify(manifest, null, 2));
console.log('✔ Build complete:', manifest);
