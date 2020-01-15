const celeb = require('../controllers/celebrity');

module.exports = (app) => {
    app.get('/', celeb.index);
    app.post('/new', celeb.create);
    app.get('/remove/:name', celeb.delete);
    app.get('/:name', celeb.show);

};