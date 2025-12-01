const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

console.log('🚀 Building FlashCards Desktop...')

// Собираем статические файлы Django
console.log('📦 Collecting Django static files...')
try {
    execSync('python ../backend/manage.py collectstatic --noinput', {
        cwd: path.join(__dirname, '..', 'frontend'),
        stdio: 'inherit'
    })
} catch (error) {
    console.log('Note: Django static collection failed (might be okay)')
}

// Создаем базу данных если нужно
console.log('🗄️  Setting up database...')
try {
    execSync('python ../backend/manage.py migrate --noinput', {
        cwd: path.join(__dirname, '..', 'frontend'),
        stdio: 'inherit'
    })
} catch (error) {
    console.log('Note: Database migration failed (might be okay)')
}

// Сборка Electron
console.log('🔨 Building Electron app...')
execSync('npm run build', {
    cwd: path.join(__dirname, '..', 'frontend'),
    stdio: 'inherit'
})

console.log('✅ Build completed!')