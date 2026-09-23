const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const rootDir = path.resolve(__dirname, '..');
const backendDir = __dirname;

// Detect python executable (prefer project venv if present)
const candidatePythons = [
  path.join(rootDir, 'venv', 'Scripts', 'python.exe'),
  path.join(rootDir, 'venv', 'bin', 'python'),
  path.join(backendDir, 'venv', 'Scripts', 'python.exe'),
  path.join(backendDir, 'venv', 'bin', 'python'),
  'python',
  'python3'
];

let pythonExe = 'python';
for (const cand of candidatePythons) {
  if (path.isAbsolute(cand) && fs.existsSync(cand)) {
    pythonExe = cand;
    break;
  }
}

const isProd = process.argv.includes('--prod');
const args = ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'];
if (!isProd) {
  args.push('--reload');
}

console.log(`\x1b[36m[Backend]\x1b[0m Starting FastAPI server using: ${pythonExe}`);
console.log(`\x1b[36m[Backend]\x1b[0m API available at http://127.0.0.1:8000`);

const child = spawn(pythonExe, args, {
  cwd: backendDir,
  stdio: 'inherit',
  env: {
    ...process.env,
    PYTHONUNBUFFERED: '1',
    PYTHONPATH: [backendDir, rootDir, process.env.PYTHONPATH].filter(Boolean).join(path.delimiter)
  }
});

child.on('error', (err) => {
  console.error('\x1b[31m[Backend Error]\x1b[0m Failed to start backend:', err);
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
