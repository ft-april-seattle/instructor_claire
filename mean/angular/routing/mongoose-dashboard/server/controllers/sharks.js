const mongoose = require('mongoose');
const Shark = require('../models/shark');
const path = require('path');

module.exports = {
    index: (req, res) => {
        Shark.find()
        .then(data => res.json(data))
        .catch(err => res.json(err));
    },
    show: (req, res) => {
        Shark.findById(req.params.id)
        .then(data => res.json(data))
        .catch(err => res.json(err));
    },
    create: (req, res) => {
        Shark.create(req.body)
        .then(data => res.json(data))
        .catch(err => res.json(err));
    },
    update: (req, res) => {
        Shark.findByIdAndUpdate(req.params.id, req.body)
        .then(data => res.json(data))
        .catch(err => res.json(err));
    },
    delete: (req, res) => {
        Shark.findByIdAndDelete(req.params.id)
        .then(data => res.json(data))
        .catch(err => res.json(err));
    },
    angular: (req,res,next) => {
        res.sendFile(path.resolve("./public/dist/public/index.html"));
    }
};