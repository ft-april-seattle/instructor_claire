const mongoose = require("mongoose");
const Task = mongoose.model("Task");

module.exports = {
    index: (req, res) => {
        console.log("In Controller!");
        Task.find()
        .then(data => res.json(data))
        .catch(err => res.json(err))
    },
    show: (req, res) => {
        Task.findById(req.params.id)
        .then(data => res.json(data))
        .catch(err => res.json(err))
    },
    create: (req, res) => {
        Task.create(req.body)
        .then(data => res.json(data))
        .catch(err => res.json(err))
    },
    update: (req, res) => {
        Task.findByIdAndUpdate(req.params.id, req.body)
        .then(data => res.json(data))
        .catch(err => res.json(err))
    },
    delete: (req, res) => {
        Task.findByIdAndDelete(req.params.id)
        .then(data => res.json(data))
        .catch(err => res.json(err))
    }
};