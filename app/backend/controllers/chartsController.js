const Record = require('../models/Record')
const fs = require('fs')
const path = require("path")

const ChartsController = {
    index: (req, res) => {
        folder_path = path.resolve('./app/frontend/views/partials/charts')
        file_list = fs.readdirSync(folder_path)
        console.log(file_list)
        res.render('charts', { file_list })
    },

    findOneByID: (req, res) => {
        chart_id = req.params.id
        chart_path = `partials/charts/${chart_id}`
        res.render('chart', { chart_path })
    }
}

module.exports = ChartsController