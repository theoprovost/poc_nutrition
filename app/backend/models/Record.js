const db = require('../database')

class Record {
    constructor(data) {
        for (const prop in data) {
            this[prop] = data[prop]
        }
    }

    static async findOneByCode(EAN_13) {
        console.log(EAN_13)
        const record = await db.query(`
            SELECT * FROM records WHERE code = '${EAN_13}'
        `)

        if (record.rows) {
            return record.rows[0]
        } else return false
    }
}

module.exports = Record