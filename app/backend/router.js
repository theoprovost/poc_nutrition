const { Router } = require('express');
const router = Router();

const mainController = require('./controllers/mainController')
const APIController = require('./controllers/APIController')
const chartsController = require('./controllers/chartsController')

router.get('/', mainController.index)

router.get('/api/search/:id', APIController.findOneByCode)

router.get('/charts', chartsController.index)
router.get('/charts/:id', chartsController.findOneByID)

router.get('*', (req, res) => res.send(404))

module.exports = router;