#!/usr/bin/env node

/**
 * Integration Verification Script
 * 
 * This script verifies the full-stack integration setup and tests communication
 * between frontend and backend when services are running.
 */

const fs = require('fs');
const path = require('path');

// ANSI color codes
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    magenta: '\x1b[35m',
    reset: '\x1b[0m'
};

function print(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkFile(filePath, description) {
    if (fs.existsSync(filePath)) {
        print(`✅ ${description}`, 'green');
        return true;
    } else {
        print(`❌ ${description} (missing: ${filePath})`, 'red');
        return false;
    }
}

function verifyProjectStructure() {
    print('\n🔍 Verifying Project Structure', 'blue');
    print('==============================', 'blue');
    
    const checks = [
        // Startup scripts
        { path: './start-dev.sh', desc: 'Unix/macOS startup script' },
        { path: './start-dev.bat', desc: 'Windows startup script' },
        { path: './start-dev.js', desc: 'Cross-platform Node.js startup script' },
        
        // Configuration files
        { path: './frontend/.env.example', desc: 'Frontend environment example' },
        { path: './backend/.env.example', desc: 'Backend environment example' },
        { path: './frontend/package.json', desc: 'Frontend package configuration' },
        { path: './backend/requirements.txt', desc: 'Backend requirements' },
        
        // Integration tests
        { path: './tests/integration/integration-test.js', desc: 'Node.js integration test' },
        { path: './tests/integration/test_fullstack_integration.py', desc: 'Python integration test' },
        { path: './test-fullstack.sh', desc: 'Bash integration test script' },
        
        // Documentation
        { path: './docs/development-workflow.md', desc: 'Development workflow documentation' },
        
        // Core application files
        { path: './backend/run.py', desc: 'Backend entry point' },
        { path: './backend/config.py', desc: 'Backend configuration' },
        { path: './frontend/src/services/api.js', desc: 'Frontend API client' },
        { path: './package.json', desc: 'Root package configuration' }
    ];
    
    let allPresent = true;
    checks.forEach(check => {
        if (!checkFile(check.path, check.desc)) {
            allPresent = false;
        }
    });
    
    return allPresent;
}

function verifyPackageJsonScripts() {
    print('\n📜 Verifying Package Scripts', 'blue');
    print('===========================', 'blue');
    
    try {
        const packageJson = JSON.parse(fs.readFileSync('./package.json', 'utf8'));
        const scripts = packageJson.scripts || {};
        
        const expectedScripts = [
            'dev',
            'dev:frontend',
            'dev:backend',
            'dev:check',
            'test:integration',
            'test:fullstack',
            'setup'
        ];
        
        let allPresent = true;
        expectedScripts.forEach(script => {
            if (scripts[script]) {
                print(`✅ npm run ${script}`, 'green');
            } else {
                print(`❌ npm run ${script} (missing)`, 'red');
                allPresent = false;
            }
        });
        
        return allPresent;
    } catch (error) {
        print(`❌ Error reading package.json: ${error.message}`, 'red');
        return false;
    }
}

function verifyConfiguration() {
    print('\n⚙️  Verifying Configuration', 'blue');
    print('===========================', 'blue');
    
    let configValid = true;
    
    // Check frontend proxy configuration
    try {
        const frontendPackage = JSON.parse(fs.readFileSync('./frontend/package.json', 'utf8'));
        if (frontendPackage.proxy === 'http://localhost:5001') {
            print('✅ Frontend proxy configured correctly', 'green');
        } else {
            print('⚠️  Frontend proxy not configured or incorrect', 'yellow');
            print(`   Expected: http://localhost:5001, Found: ${frontendPackage.proxy}`, 'yellow');
        }
    } catch (error) {
        print('❌ Error checking frontend proxy configuration', 'red');
        configValid = false;
    }
    
    // Check backend CORS configuration
    try {
        const configFile = fs.readFileSync('./backend/config.py', 'utf8');
        if (configFile.includes('CORS_ORIGINS') && configFile.includes('localhost:3000')) {
            print('✅ Backend CORS configuration found', 'green');
        } else {
            print('❌ Backend CORS configuration missing or incorrect', 'red');
            configValid = false;
        }
    } catch (error) {
        print('❌ Error checking backend CORS configuration', 'red');
        configValid = false;
    }
    
    // Check API client configuration
    try {
        const apiFile = fs.readFileSync('./frontend/src/services/api.js', 'utf8');
        if (apiFile.includes('getApiBaseUrl') && apiFile.includes('localhost:5001')) {
            print('✅ Frontend API client configured correctly', 'green');
        } else {
            print('❌ Frontend API client configuration incorrect', 'red');
            configValid = false;
        }
    } catch (error) {
        print('❌ Error checking API client configuration', 'red');
        configValid = false;
    }
    
    return configValid;
}

async function testServiceConnectivity() {
    print('\n🌐 Testing Service Connectivity', 'blue');
    print('==============================', 'blue');
    
    try {
        const axios = require('axios');
        
        // Test backend health
        try {
            const backendResponse = await axios.get('http://localhost:5001/api/health', { timeout: 3000 });
            if (backendResponse.status === 200 && backendResponse.data.status === 'healthy') {
                print('✅ Backend API is accessible and healthy', 'green');
                print(`   Response: ${backendResponse.data.message}`, 'cyan');
                
                // Test CORS headers
                const corsResponse = await axios.get('http://localhost:5001/api/health', {
                    headers: { 'Origin': 'http://localhost:3000' },
                    timeout: 3000
                });
                
                if (corsResponse.headers['access-control-allow-origin']) {
                    print('✅ CORS headers are properly configured', 'green');
                } else {
                    print('⚠️  CORS headers not detected', 'yellow');
                }
                
                return true;
            } else {
                print('❌ Backend API returned unexpected response', 'red');
                return false;
            }
        } catch (error) {
            if (error.code === 'ECONNREFUSED') {
                print('⚠️  Backend is not running on port 5001', 'yellow');
                print('   Start with: npm run dev:backend', 'cyan');
            } else {
                print(`❌ Backend connectivity error: ${error.message}`, 'red');
            }
            return false;
        }
        
    } catch (error) {
        print('⚠️  axios not available for connectivity test', 'yellow');
        print('   Install with: npm install', 'cyan');
        return false;
    }
}

function showUsageInstructions() {
    print('\n🚀 Usage Instructions', 'blue');
    print('====================', 'blue');
    
    print('\n1. Install dependencies:', 'cyan');
    print('   npm install', 'reset');
    
    print('\n2. Setup the project:', 'cyan');
    print('   npm run setup', 'reset');
    
    print('\n3. Start development environment:', 'cyan');
    print('   npm run dev                 # Recommended: Node.js script', 'reset');
    print('   ./start-dev.sh             # Unix/macOS bash script', 'reset');
    print('   start-dev.bat              # Windows batch script', 'reset');
    
    print('\n4. Run integration tests:', 'cyan');
    print('   npm run test:integration   # Node.js integration test', 'reset');
    print('   npm run test:fullstack     # Complete bash test script', 'reset');
    
    print('\n5. Access the application:', 'cyan');
    print('   Frontend: http://localhost:3000', 'reset');
    print('   Backend:  http://localhost:5001/api', 'reset');
    print('   Health:   http://localhost:5001/api/health', 'reset');
    
    print('\n6. Development commands:', 'cyan');
    print('   npm run dev:check          # Check service status', 'reset');
    print('   npm run dev:frontend       # Start frontend only', 'reset');
    print('   npm run dev:backend        # Start backend only', 'reset');
    print('   npm run health             # Quick health check', 'reset');
}

function showTroubleshootingTips() {
    print('\n🔧 Troubleshooting Tips', 'yellow');
    print('======================', 'yellow');
    
    print('\n• Port conflicts:', 'yellow');
    print('  - Check: lsof -i :5001 -i :3000', 'reset');
    print('  - Kill: npm run dev:check && ./start-dev.sh --stop', 'reset');
    
    print('\n• Dependency issues:', 'yellow');
    print('  - Clean: npm run clean:all && npm run setup', 'reset');
    
    print('\n• Database issues:', 'yellow');
    print('  - Reset: npm run db:reset', 'reset');
    
    print('\n• CORS errors:', 'yellow');
    print('  - Check backend config.py CORS_ORIGINS setting', 'reset');
    print('  - Verify frontend proxy in package.json', 'reset');
    
    print('\n• Integration test failures:', 'yellow');
    print('  - Ensure both services are running first', 'reset');
    print('  - Check logs: npm run logs:backend', 'reset');
}

async function main() {
    print('🔍 Full-Stack Integration Verification', 'magenta');
    print('======================================', 'magenta');
    
    print('\nThis script verifies that the full-stack integration is properly configured.', 'reset');
    
    // Run verification checks
    const structureValid = verifyProjectStructure();
    const scriptsValid = verifyPackageJsonScripts();
    const configValid = verifyConfiguration();
    const connectivityWorking = await testServiceConnectivity();
    
    // Summary
    print('\n📊 Verification Summary', 'blue');
    print('======================', 'blue');
    
    const checks = [
        { name: 'Project Structure', passed: structureValid },
        { name: 'Package Scripts', passed: scriptsValid },
        { name: 'Configuration', passed: configValid },
        { name: 'Service Connectivity', passed: connectivityWorking }
    ];
    
    checks.forEach(check => {
        const icon = check.passed ? '✅' : '❌';
        const color = check.passed ? 'green' : 'red';
        print(`${icon} ${check.name}`, color);
    });
    
    const allPassed = checks.every(check => check.passed);
    
    if (allPassed) {
        print('\n🎉 Integration verification successful!', 'green');
        print('Your full-stack environment is properly configured.', 'green');
        
        if (connectivityWorking) {
            print('\n✨ Services are running and communicating correctly!', 'green');
            print('You can now run: npm run test:integration', 'cyan');
        }
    } else {
        print('\n⚠️  Some verification checks failed.', 'yellow');
        
        if (!connectivityWorking && structureValid) {
            print('Configuration looks good, but services are not running.', 'yellow');
            print('Start services with: npm run dev', 'cyan');
        }
    }
    
    showUsageInstructions();
    
    if (!allPassed || !connectivityWorking) {
        showTroubleshootingTips();
    }
    
    print('\n📚 For detailed documentation, see:', 'blue');
    print('   docs/development-workflow.md', 'cyan');
}

// Handle errors gracefully
process.on('unhandledRejection', (error) => {
    print(`\n❌ Unexpected error: ${error.message}`, 'red');
    process.exit(1);
});

// Run the verification
main().catch(error => {
    print(`❌ Error: ${error.message}`, 'red');
    process.exit(1);
});