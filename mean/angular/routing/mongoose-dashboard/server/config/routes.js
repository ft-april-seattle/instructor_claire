const sharks = require('../controllers/sharks');

module.exports = (app) => {
    app.get("/api/sharks", sharks.index);
    app.get("/api/sharks/:id", sharks.show);
    app.post("/api/sharks", sharks.create);
    app.put("/api/sharks/:id", sharks.update);
    app.delete("/api/sharks/:id", sharks.delete);
    app.all("*", sharks.angular);
};