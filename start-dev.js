#!/usr/bin/env node

/**
 * Cross-platform Development Environment Startup Script
 * This script starts both the backend Flask server and frontend React development server
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const net = require('net');
const readline = require('readline');

// Configuration
const PROJECT_ROOT = __dirname;
const BACKEND_DIR = path.join(PROJECT_ROOT, 'backend');
const FRONTEND_DIR = path.join(PROJECT_ROOT, 'frontend');
const BACKEND_PORT = 5001;
const FRONTEND_PORT = 3000;
const BACKEND_LOG = path.join(BACKEND_DIR, 'logs', 'backend.log');
const FRONTEND_LOG = path.join(FRONTEND_DIR, 'logs', 'frontend.log');

// ANSI color codes
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    reset: '\x1b[0m'
};

// Helper functions
function print(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function printStatus(icon, message, color) {
    print(`${icon} ${message}`, color);
}

function ensureDirectoryExists(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function commandExists(command) {
    try {
        execSync(`${process.platform === 'win32' ? 'where' : 'which'} ${command}`, { stdio: 'ignore' });
        return true;
    } catch {
        return false;
    }
}

function isPortInUse(port) {
    return new Promise((resolve) => {
        const server = net.createServer();
        server.once('error', () => resolve(true));
        server.once('listening', () => {
            server.close();
            resolve(false);
        });
        server.listen(port);
    });
}

async function killProcessOnPort(port) {
    if (await isPortInUse(port)) {
        print(`Port ${port} is in use. Attempting to kill process...`, 'yellow');
        try {
            if (process.platform === 'win32') {
                execSync(`for /f "tokens=5" %a in ('netstat -aon ^| findstr :${port}') do taskkill /F /PID %a`, { stdio: 'ignore' });
            } else {
                execSync(`lsof -ti:${port} | xargs kill -9`, { stdio: 'ignore' });
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        } catch {
            // Ignore errors
        }
    }
}

async function waitForPort(port, timeout = 30000) {
    const startTime = Date.now();
    while (Date.now() - startTime < timeout) {
        if (await isPortInUse(port)) {
            return true;
        }
        await new Promise(resolve => setTimeout(resolve, 1000));
        process.stdout.write('.');
    }
    process.stdout.write('\n');
    return false;
}

// Check requirements
function checkRequirements() {
    print('\n🔍 Checking requirements...', 'blue');
    
    const requirements = [
        { command: 'node', name: 'Node.js', version: 'node --version' },
        { command: process.platform === 'win32' ? 'python' : 'python3', name: 'Python', version: 'python --version' },
        { command: 'npm', name: 'npm', version: 'npm --version' }
    ];
    
    let allMet = true;
    
    for (const req of requirements) {
        if (commandExists(req.command)) {
            try {
                const version = execSync(req.version, { encoding: 'utf8' }).trim();
                printStatus('✅', `${req.name} found: ${version}`, 'green');
            } catch {
                printStatus('✅', `${req.name} found`, 'green');
            }
        } else {
            printStatus('❌', `${req.name} is not installed`, 'red');
            allMet = false;
        }
    }
    
    if (!allMet) {
        print('\n❌ Please install missing requirements and try again.', 'red');
        process.exit(1);
    }
    
    printStatus('✅', 'All requirements met', 'green');
}

// Setup environment
async function setupEnvironment() {
    print('\n🔧 Setting up environment...', 'blue');
    
    // Create log directories
    ensureDirectoryExists(path.join(BACKEND_DIR, 'logs'));
    ensureDirectoryExists(path.join(FRONTEND_DIR, 'logs'));
    
    // Check virtual environment
    const venvPath = path.join(BACKEND_DIR, 'venv');
    if (!fs.existsSync(venvPath)) {
        print('⚠️  Virtual environment not found. Creating...', 'yellow');
        execSync(`cd "${BACKEND_DIR}" && ${process.platform === 'win32' ? 'python' : 'python3'} -m venv venv`, { stdio: 'inherit' });
    }
    
    // Check backend dependencies
    const pipPath = process.platform === 'win32' 
        ? path.join(venvPath, 'Scripts', 'pip.exe')
        : path.join(venvPath, 'bin', 'pip');
    
    try {
        execSync(`"${pipPath}" show flask`, { stdio: 'ignore' });
    } catch {
        print('⚠️  Backend dependencies not installed. Installing...', 'yellow');
        execSync(`cd "${BACKEND_DIR}" && "${pipPath}" install -r requirements.txt`, { stdio: 'inherit' });
    }
    
    // Check frontend dependencies
    if (!fs.existsSync(path.join(FRONTEND_DIR, 'node_modules'))) {
        print('⚠️  Frontend dependencies not installed. Installing...', 'yellow');
        execSync(`cd "${FRONTEND_DIR}" && npm install`, { stdio: 'inherit' });
    }
    
    // Initialize database
    const dbPath = path.join(BACKEND_DIR, 'instance', 'todo_dev.db');
    if (!fs.existsSync(dbPath)) {
        print('⚠️  Database not found. Initializing...', 'yellow');
        const pythonPath = process.platform === 'win32'
            ? path.join(venvPath, 'Scripts', 'python.exe')
            : path.join(venvPath, 'bin', 'python');
        
        const initDbScript = `
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database initialized!')
`;
        execSync(`cd "${BACKEND_DIR}" && "${pythonPath}" -c "${initDbScript}"`, { stdio: 'inherit' });
    }
    
    printStatus('✅', 'Environment setup complete', 'green');
}

// Start backend server
async function startBackend() {
    print('\n🚀 Starting Flask backend...', 'cyan');
    
    await killProcessOnPort(BACKEND_PORT);
    
    const pythonPath = process.platform === 'win32'
        ? path.join(BACKEND_DIR, 'venv', 'Scripts', 'python.exe')
        : path.join(BACKEND_DIR, 'venv', 'bin', 'python');
    
    const env = {
        ...process.env,
        FLASK_APP: 'run.py',
        FLASK_ENV: 'development',
        FLASK_DEBUG: '1'
    };
    
    const backendLogStream = fs.createWriteStream(BACKEND_LOG, { flags: 'a' });
    
    const backend = spawn(pythonPath, ['run.py'], {
        cwd: BACKEND_DIR,
        env,
        shell: process.platform === 'win32'
    });
    
    backend.stdout.pipe(backendLogStream);
    backend.stderr.pipe(backendLogStream);
    
    backend.on('error', (err) => {
        printStatus('❌', `Backend error: ${err.message}`, 'red');
    });
    
    process.stdout.write('Waiting for backend to start');
    if (await waitForPort(BACKEND_PORT)) {
        printStatus('✅', `Backend started on port ${BACKEND_PORT} (PID: ${backend.pid})`, 'green');
        return backend;
    } else {
        printStatus('❌', 'Failed to start backend', 'red');
        backend.kill();
        process.exit(1);
    }
}

// Start frontend server
async function startFrontend() {
    print('\n🚀 Starting React frontend...', 'cyan');
    
    await killProcessOnPort(FRONTEND_PORT);
    
    const env = {
        ...process.env,
        PORT: FRONTEND_PORT.toString(),
        BROWSER: 'none'
    };
    
    const frontendLogStream = fs.createWriteStream(FRONTEND_LOG, { flags: 'a' });
    
    const npmCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
    const frontend = spawn(npmCmd, ['start'], {
        cwd: FRONTEND_DIR,
        env,
        shell: process.platform === 'win32'
    });
    
    frontend.stdout.pipe(frontendLogStream);
    frontend.stderr.pipe(frontendLogStream);
    
    frontend.on('error', (err) => {
        printStatus('❌', `Frontend error: ${err.message}`, 'red');
    });
    
    process.stdout.write('Waiting for frontend to start');
    if (await waitForPort(FRONTEND_PORT, 60000)) {
        printStatus('✅', `Frontend started on port ${FRONTEND_PORT} (PID: ${frontend.pid})`, 'green');
        return frontend;
    } else {
        printStatus('❌', 'Failed to start frontend', 'red');
        frontend.kill();
        process.exit(1);
    }
}

// Show status
function showStatus() {
    print('\n📊 Development Environment Status', 'blue');
    print('=================================', 'blue');
    
    print('\n✅ Backend:  http://localhost:' + BACKEND_PORT, 'green');
    print('   API:      http://localhost:' + BACKEND_PORT + '/api', 'green');
    print('   Health:   http://localhost:' + BACKEND_PORT + '/api/health', 'green');
    
    print('\n✅ Frontend: http://localhost:' + FRONTEND_PORT, 'green');
    
    print('\n📝 Logs:', 'blue');
    print('  Backend:  ' + BACKEND_LOG, 'blue');
    print('  Frontend: ' + FRONTEND_LOG, 'blue');
    
    print('\n🛠️  Commands:', 'blue');
    print('  View backend logs:  tail -f ' + BACKEND_LOG, 'blue');
    print('  View frontend logs: tail -f ' + FRONTEND_LOG, 'blue');
    print('  Stop all:          Press Ctrl+C', 'blue');
}

// Main function
async function main() {
    print('🚀 Starting Development Environment', 'blue');
    print('==================================\n', 'blue');
    
    checkRequirements();
    await setupEnvironment();
    
    const backend = await startBackend();
    const frontend = await startFrontend();
    
    showStatus();
    
    print('\n✨ Development environment is ready!', 'green');
    print('   Frontend: http://localhost:' + FRONTEND_PORT, 'green');
    print('   Backend:  http://localhost:' + BACKEND_PORT + '/api', 'green');
    
    // Handle graceful shutdown
    const cleanup = () => {
        print('\n\n🛑 Shutting down development environment...', 'yellow');
        
        backend.kill();
        print('   Stopped backend (PID: ' + backend.pid + ')', 'yellow');
        
        frontend.kill();
        print('   Stopped frontend (PID: ' + frontend.pid + ')', 'yellow');
        
        printStatus('✅', 'Shutdown complete', 'green');
        process.exit(0);
    };
    
    process.on('SIGINT', cleanup);
    process.on('SIGTERM', cleanup);
    
    // Keep the process running
    print('\n📋 Press Ctrl+C to stop all services...', 'yellow');
    
    // Create interface for interactive commands
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    rl.on('line', (input) => {
        const command = input.trim().toLowerCase();
        
        switch (command) {
            case 'status':
                showStatus();
                break;
            case 'help':
                print('\nAvailable commands:', 'blue');
                print('  status - Show current status', 'blue');
                print('  help   - Show this help', 'blue');
                print('  exit   - Stop all services and exit', 'blue');
                break;
            case 'exit':
            case 'quit':
                cleanup();
                break;
            default:
                if (command) {
                    print(`Unknown command: ${command}. Type 'help' for available commands.`, 'yellow');
                }
        }
    });
}

// Parse command line arguments
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    print('Development Environment Startup Script', 'blue');
    print('');
    print('Usage: node start-dev.js [options]');
    print('');
    print('Options:');
    print('  --help, -h        Show this help message');
    print('  --backend-only    Start only the backend server');
    print('  --frontend-only   Start only the frontend server');
    print('  --check           Check if services are running');
    print('');
    process.exit(0);
}

if (args.includes('--check')) {
    Promise.all([
        isPortInUse(BACKEND_PORT),
        isPortInUse(FRONTEND_PORT)
    ]).then(([backendRunning, frontendRunning]) => {
        print('\n📊 Service Status', 'blue');
        print('=================', 'blue');
        
        if (backendRunning) {
            print('✅ Backend is running on port ' + BACKEND_PORT, 'green');
        } else {
            print('❌ Backend is not running', 'red');
        }
        
        if (frontendRunning) {
            print('✅ Frontend is running on port ' + FRONTEND_PORT, 'green');
        } else {
            print('❌ Frontend is not running', 'red');
        }
        
        process.exit(0);
    });
} else if (args.includes('--backend-only')) {
    checkRequirements();
    setupEnvironment().then(() => {
        startBackend().then(() => {
            showStatus();
            print('\nBackend running (Press Ctrl+C to stop)...', 'yellow');
        });
    });
} else if (args.includes('--frontend-only')) {
    checkRequirements();
    setupEnvironment().then(() => {
        startFrontend().then(() => {
            showStatus();
            print('\nFrontend running (Press Ctrl+C to stop)...', 'yellow');
        });
    });
} else {
    main().catch(err => {
        printStatus('❌', `Error: ${err.message}`, 'red');
        process.exit(1);
    });
}