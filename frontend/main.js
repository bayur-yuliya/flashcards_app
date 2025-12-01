const { app, BrowserWindow, dialog } = require('electron')
const { spawn } = require('child_process')
const path = require('path')
const fs = require('fs')

console.log('=== FlashCards Desktop запускается ===')

let mainWindow
let djangoProcess

function createWindow() {
    console.log('Создаем главное окно...')

    try {
        mainWindow = new BrowserWindow({
            width: 1200,
            height: 800,
            minWidth: 800,
            minHeight: 600,
            show: false,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                webSecurity: false
            }
        })

        console.log('Окно создано успешно')

        mainWindow.once('ready-to-show', () => {
            console.log('Окно готово к показу')
            mainWindow.show()
        })

        // Сначала показываем страницу загрузки
        showLoadingPage()

        // Запускаем Django сервер
        setTimeout(() => {
            startDjangoServer()
        }, 500)

    } catch (error) {
        console.error('ОШИБКА при создании окна:', error)
        dialog.showErrorBox('Ошибка', 'Не удалось создать окно приложения.')
    }
}

function showLoadingPage() {
    console.log('Показываем страницу загрузки...')

    const loadingHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Загрузка...</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #667eea;
                    color: white;
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .container {
                    text-align: center;
                }
                .spinner {
                    border: 8px solid rgba(255,255,255,0.3);
                    border-radius: 50%;
                    border-top: 8px solid white;
                    width: 60px;
                    height: 60px;
                    animation: spin 1s linear infinite;
                    margin: 30px auto;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>FlashCards Desktop</h1>
                <p>Запуск приложения...</p>
                <div class="spinner"></div>
                <p>Пожалуйста, подождите</p>
            </div>
        </body>
        </html>
    `

    mainWindow.loadURL('data:text/html;charset=utf-8,' + encodeURI(loadingHTML))
}

function startDjangoServer() {
    console.log('=== ПОИСК BACKEND ===')
    console.log('Текущая папка:', __dirname)
    console.log('Ресурсы приложения:', process.resourcesPath)
    console.log('App is packaged:', app.isPackaged)

    // ВАЖНО: Проверяем разные пути где может быть backend
    const searchPaths = []

    // Если приложение собрано
    if (app.isPackaged) {
        // 1. В папке с exe файлом
        searchPaths.push(path.join(process.cwd(), 'backend'))
        // 2. В папке resources (старый способ)
        searchPaths.push(path.join(process.resourcesPath, 'backend'))
        // 3. На один уровень выше
        searchPaths.push(path.join(process.cwd(), '..', 'backend'))
        searchPaths.push(path.join(process.cwd(), '..', '..', 'backend'))
        // 4. В app.asar.unpacked
        searchPaths.push(path.join(process.resourcesPath, 'app.asar.unpacked', 'backend'))
    } else {
        // Режим разработки
        searchPaths.push(path.join(__dirname, '..', 'backend'))
        searchPaths.push(path.join(process.cwd(), 'backend'))
    }

    console.log('Ищем backend в следующих местах:')
    let backendPath = null
    let managePyPath = null

    for (const searchPath of searchPaths) {
        const possibleManagePy = path.join(searchPath, 'manage.py')
        console.log(`  Проверяем: ${searchPath}`)
        console.log(`    Файл: ${possibleManagePy}`)
        console.log(`    Существует: ${fs.existsSync(possibleManagePy)}`)

        if (fs.existsSync(possibleManagePy)) {
            backendPath = searchPath
            managePyPath = possibleManagePy
            console.log(`✅ НАЙДЕНО! В: ${backendPath}`)
            break
        }
    }

    // Если не нашли - посмотрим что вообще есть в папках
    if (!backendPath) {
        console.log('=== СОДЕРЖИМОЕ ПАПОК ===')

        // Проверим папку с exe
        const exeDir = process.cwd()
        console.log(`Содержимое ${exeDir}:`)
        try {
            const files = fs.readdirSync(exeDir)
            files.forEach(file => {
                const fullPath = path.join(exeDir, file)
                const isDir = fs.statSync(fullPath).isDirectory()
                console.log(`  ${isDir ? '📁' : '📄'} ${file}`)
            })
        } catch (e) {
            console.log('Не удалось прочитать папку:', e.message)
        }

        // Проверим папку ресурсов
        console.log(`Содержимое ${process.resourcesPath}:`)
        try {
            const files = fs.readdirSync(process.resourcesPath)
            files.forEach(file => {
                const fullPath = path.join(process.resourcesPath, file)
                const isDir = fs.statSync(fullPath).isDirectory()
                console.log(`  ${isDir ? '📁' : '📄'} ${file}`)
            })
        } catch (e) {
            console.log('Не удалось прочитать ресурсы:', e.message)
        }

        showError('Backend не найден',
            'Папка "backend" с Django проектом не найдена.\n\n' +
            'Проверьте что папка backend находится в правильном месте.'
        )
        return
    }

    console.log(`✅ Используем backend из: ${backendPath}`)
    console.log(`✅ Файл manage.py: ${managePyPath}`)

    // Запускаем Django
    console.log('Запускаем Django сервер...')

    try {
        // Проверяем Python
        spawn('python', ['--version'])
        console.log('✅ Python найден')

        // Запускаем Django
        djangoProcess = spawn('python', [
            managePyPath,
            'runserver',
            '8000',
            '--noreload'
        ], {
            cwd: backendPath,
            shell: true
        })

        djangoProcess.stdout.on('data', (data) => {
            const output = data.toString()
            console.log('Django:', output)

            if (output.includes('Starting development server')) {
                console.log('✅ Django сервер запускается...')

                // Через 2 секунды пробуем загрузить
                setTimeout(() => {
                    loadDjangoApp()
                }, 2000)
            }
        })

        djangoProcess.stderr.on('data', (data) => {
            const error = data.toString()
            console.error('Django ошибка:', error)
        })

        djangoProcess.on('error', (error) => {
            console.error('Не запустился Django:', error)
            showError('Ошибка Django', error.message)
        })

        // Таймаут 15 секунд
        setTimeout(() => {
            console.log('Таймаут, пробуем загрузить...')
            loadDjangoApp()
        }, 15000)

    } catch (error) {
        console.error('Ошибка Python:', error)
        showError('Python не найден',
            'Установите Python с python.org и добавьте в PATH'
        )
    }
}

function loadDjangoApp() {
    console.log('Пробуем загрузить http://localhost:8000...')

    mainWindow.loadURL('http://localhost:8000')
        .then(() => {
            console.log('✅ Успешно загружено!')
        })
        .catch((error) => {
            console.error('❌ Ошибка загрузки:', error.message)
            showErrorPage()
        })
}

function showErrorPage() {
    const errorHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Ошибка</title>
            <style>
                body {
                    font-family: Arial;
                    padding: 40px;
                    text-align: center;
                }
                .error {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 30px;
                    border: 2px solid red;
                    border-radius: 10px;
                }
                button {
                    background: blue;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 10px;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div class="error">
                <h1>Ошибка запуска</h1>
                <p>Не удалось запустить приложение.</p>
                <p>Возможно, Django сервер не запустился.</p>
                <button onclick="location.reload()">Попробовать снова</button>
                <button onclick="window.close()">Закрыть</button>
            </div>
        </body>
        </html>
    `

    mainWindow.loadURL('data:text/html;charset=utf-8,' + encodeURI(errorHTML))
}

function showError(title, message) {
    console.error(`Ошибка: ${title} - ${message}`)

    if (mainWindow) {
        dialog.showMessageBox(mainWindow, {
            type: 'error',
            title: title,
            message: message,
            buttons: ['OK']
        })
    } else {
        dialog.showErrorBox(title, message)
    }
}

// События приложения
app.whenReady().then(() => {
    console.log('App ready, создаем окно...')
    createWindow()
})

app.on('window-all-closed', () => {
    if (djangoProcess) {
        djangoProcess.kill()
    }
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('before-quit', () => {
    if (djangoProcess) {
        djangoProcess.kill()
    }
})

console.log('Скрипт загружен, ждем ready...')