const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const rootDir = __dirname;
const backendDir = path.join(rootDir, 'backend');
const frontendDir = path.join(rootDir, 'frontend');

// Detect python executable for backend
const candidatePythons = [
  path.join(rootDir, 'venv', 'Scripts', 'python.exe'),
  path.join(rootDir, 'venv', 'bin', 'python'),
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

console.log('\x1b[35m=====================================================\x1b[0m');
console.log('\x1b[35m  Starting DeepFake Detection Platform (Fullstack)   \x1b[0m');
console.log('\x1b[35m=====================================================\x1b[0m');

// Spawn Backend
const backend = spawn(pythonExe, ['-m', 'uvicorn', 'backend.main:app', '--reload', '--host', '127.0.0.1', '--port', '8000'], {
  cwd: rootDir,
  stdio: 'inherit',
  env: {
    ...process.env,
    PYTHONUNBUFFERED: '1',
    PYTHONPATH: [rootDir, backendDir, process.env.PYTHONPATH].filter(Boolean).join(path.delimiter)
  }
});

// Spawn Frontend
const isWin = process.platform === 'win32';
const npmCmd = isWin ? 'npm.cmd' : 'npm';
const frontend = spawn(npmCmd, ['run', 'dev'], {
  cwd: frontendDir,
  stdio: 'inherit'
});

function cleanup() {
  console.log('\n\x1b[33mShutting down servers...\x1b[0m');
  try { backend.kill(); } catch (e) {}
  try { frontend.kill(); } catch (e) {}
  process.exit(0);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
