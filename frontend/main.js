const { app, BrowserWindow, dialog } = require('electron')
const { spawn } = require('child_process')
const path = require('path')
const fs = require('fs')

let mainWindow
let djangoProcess

// Отключаем проблемные функции
app.disableHardwareAcceleration()
app.commandLine.appendSwitch('--disable-gpu')
app.commandLine.appendSwitch('--no-sandbox')

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false
        },
        show: false,
        title: 'FlashCards Desktop'
    })

    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
    })

    startDjangoServer()
}

function startDjangoServer() {
    // Пробуем разные возможные пути к manage.py
    const possiblePaths = [
        path.join(__dirname, '..', 'flashcards_app', 'manage.py'),           // если frontend отдельно
        path.join(__dirname, '..', 'manage.py'),                             // если frontend в корне
        path.join(__dirname, '..', '..', 'flashcards_app', 'manage.py'),     // если глубже
        path.join(process.cwd(), 'flashcards_app', 'manage.py'),             // от текущей рабочей директории
        path.join(process.cwd(), 'manage.py')                                // прямо в корне
    ]

    let managePyPath = null
    let backendPath = null

    // Ищем существующий manage.py
    for (const possiblePath of possiblePaths) {
        if (fs.existsSync(possiblePath)) {
            managePyPath = possiblePath
            backendPath = path.dirname(possiblePath)
            console.log('Found manage.py at:', managePyPath)
            break
        }
    }

    if (!managePyPath) {
        console.error('Could not find manage.py file!')
        showErrorDialog('Файл manage.py не найден! Проверьте структуру проекта.')
        return
    }

    console.log('Starting Django from:', managePyPath)
    console.log('Backend directory:', backendPath)

    try {
        djangoProcess = spawn('python', [managePyPath, 'runserver', '8000', '--noreload'], {
            cwd: backendPath,
            stdio: ['pipe', 'pipe', 'pipe']
        })

        let djangoReady = false

        djangoProcess.stdout.on('data', (data) => {
            const output = data.toString()
            console.log(`Django: ${output}`)

            if (output.includes('Starting development server')) {
                console.log('Django server is starting...')
            }

            if (output.includes('Quit the server with CTRL-BREAK')) {
                console.log('Django server ready!')
                djangoReady = true
                loadDjangoApp()
            }
        })

        djangoProcess.stderr.on('data', (data) => {
            console.error(`Django Error: ${data}`)
        })

        djangoProcess.on('error', (error) => {
            console.error('Failed to start Django process:', error)
            showErrorDialog(`Ошибка запуска Django: ${error.message}`)
        })

        // Загрузка приложения через 4 секунды
        setTimeout(() => {
            if (!djangoReady) {
                console.log('Loading Django app after timeout...')
                loadDjangoApp()
            }
        }, 4000)

    } catch (error) {
        console.error('Error starting Django:', error)
        showErrorDialog(`Ошибка: ${error.message}`)
    }
}

function loadDjangoApp() {
    mainWindow.loadURL('http://localhost:8000')
        .then(() => {
            console.log('Successfully loaded Django app')
        })
        .catch((error) => {
            console.log('Failed to load Django app:', error)
            mainWindow.loadFile('error.html')
        })
}

function showErrorDialog(message) {
    dialog.showErrorBox('Ошибка запуска',
        `${message}\n\nПроверьте:\n` +
        `1. Существует ли файл manage.py\n` +
        `2. Активировано ли виртуальное окружение Python\n` +
        `3. Установлены ли Django зависимости\n` +
        `4. Структуру папок проекта`
    )
}

app.whenReady().then(createWindow)

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