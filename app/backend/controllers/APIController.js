const Record = require('../models/Record')

const APIController = {
    findOneByCode: async (req, res) => {
        const code = req.params.id
        console.log('CODE', code)
        const record = await Record.findOneByCode(code)

        if (record) {
            res.status(200).json({
                'code': 200,
                'data': record
            })
        } else {
            res.status(404).json({
                'code': 404,
                'message': 'Aucun produit ne correspond à ce code barre dans notre catalogue.'
            })
        }
    }
}

module.exports = APIController