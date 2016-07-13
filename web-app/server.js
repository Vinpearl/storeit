import express from 'express'

let app = express()

app.use(express.static('src'))
app.use('/jspm_packages', express.static('./jspm_packages'))
app.use('/jspm.browser.js', express.static('./jspm.browser.js'))
app.use('/jspm.config.js', express.static('./jspm.config.js'))

app.listen(3000)
console.log('Express server listening on port 3000')
