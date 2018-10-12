const {readdir, readFile, stat} = require("fs").promises; // Experimental API (will show a warning)
const {join} = require("path");
const express = require("express");

/**
 * Returns an array of folder names as strings for a given path
 *
 * @param path {String}
 * @returns {Promise<Array>}
 */
const get_folders = async path => {
    let folders = [];
    for (const file of await get_files(path)) {
        if ((await stat(join(path, file))).isDirectory()) {
            folders = [...folders, file]
        }
    }
    return folders
};

/**
 * Returns an array of file names as strings for a given path
 *
 * @param path {String}
 * @returns {Promise<Array>}
 */
const get_files = async path => {
    return await readdir(path);
};


/**
 * Return a file paths for a given query (not recursive)
 *
 * @param path {String}
 * @param query {String}
 * @returns {Array}
 */
const send_file = async (path, query) => {
    const first_letter = query.charAt(0);
    for (const file of await get_files(join(path, first_letter))) {
        if (file.match(new RegExp(`^${query}`, 'gi'))) { // Match from start
            return JSON.parse(await readFile(join(__dirname, first_letter, file)))
        }
    }
};

/**
 * Return file paths for a given query (recursive)
 *
 * @param folders {Array}
 * @param query {String}
 * @returns {Array}
 */
const search_files = async (folders, query) => {
    const files = [];
    for (const folder of folders) {
        for (const file of await get_files(folder)) {
            if (file.match(new RegExp(query, 'gi'))) {
                files.push(file)
            }
        }
    }
    return files;
};

(async () => { // Self-Executing Anonymous Async Function (main)

    // Get an array of our letters
    let folders = await get_folders(__dirname);
    folders = folders.filter(d => d.length === 1);

    // Bootstrap express server
    const api = express();

    // Routes
    api.get('/', (req, res) => {
        return res.send('hello world');
    });

    api.get('/:query', async (req, res) => {
        const query = req.params.query;

        switch (query.length) {

            // If the query length is one then serve a list of words
            case 1:
                return res.send(await get_files(join(__dirname, query.toUpperCase())));

            // If the query is longer than one then assume we want a word
            default:
                return res.send(await send_file(__dirname, query));
        }
    });

    api.get('/search/:query', async (req, res) => { // Fuzzy search
        const query = req.params.query;
        return res.send(await search_files(folders, query))
    });

    // Launch
    api.listen(process.env.PORT || 3000, function () {
        console.log('API Started')
    })
})();

