require('dotenv').config() // Needs to stay first

const path = require('path')
const fs = require('fs')
//const https = require('https')
const express = require('express')
const router = require('./router.js')
const cors = require('cors')


const app = express()
const port = process.env.PORT || 8443

app.use(express.json())

app.use((_, res, next) => {
    res.header("Access-Control-Allow-Origin", 'https://poc-nutrition.herokuapp.com/')
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    next();
});

// Local static assets access
app.use(express.static(path.join('./app/frontend/assets')));

// Views
app.set('views', path.join('./app/frontend/views'));
app.set('view engine', 'ejs');


app.use(router)

// HTTPS support
//const key = fs.readFileSync('./app/app/backend/keys/key.pem')
//const cert = fs.readFileSync('./app/app/backend/keys/cert.pem');
//const httpsServer = https.createServer({ key: key, cert: cert }, app)

app.listen(port, () => console.log(`Server is listening on http://localhost:${port}`));

// NB : DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process
process.on('unhandledRejection', (err) => {
    console.log('Interception d\'un rejet de promesse');
    console.error(err);
});

module.exports = app;