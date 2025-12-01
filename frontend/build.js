const { execSync } = require('child_process')
const path = require('path')

console.log('🚀 Building FlashCards Desktop...')

// Меняем текущую директорию на временную без кириллицы
process.chdir('C:\\temp\\electron-build')

// Запускаем сборку
try {
    execSync('electron-builder', {
        stdio: 'inherit',
        cwd: path.resolve(__dirname)
    })
    console.log('✅ Build successful!')
} catch (error) {
    console.error('❌ Build failed:', error.message)
    process.exit(1)
}