const { Client } = require('pg');

let client;
if (process.env.NODE_ENV && process.env.NODE_ENV === "dev") { // prod
    try {
        client = new Client({
            connectionString: process.env.DATABASE_URL
        })
        client.connect()
    } catch (error) {
        throw new Error(error);
    }
}


module.exports = client;