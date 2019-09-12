const express = require('express');
const mongoose = require('mongoose');
const app = express(); // similar to flask, app = Flask(__name__)

app.use(express.static(__dirname + "/static")); // creates path to static directory for express to look into
// "use" for middleware
app.set('view engine', 'ejs');
app.set('views', __dirname + "/views"); // "set" manages environment

app.get('/cats', (req, res) => {
    res.render('show_all');

});
app.get('/cats/:name', (req, res) => {
    const kitty_info = {
        name: req.params.name,
        fav_food: "Meow Mix",
        age: 20,
        sleeping: ["couch", "downstairs futon", "a bed"]
    };
    kitty_info.sleeping.push("windowsill");
    console.log(kitty_info);
    res.render('show_one',{kitty: kitty_info});
});

app.listen(8000, () => {
    return "listening on port 8000";
});