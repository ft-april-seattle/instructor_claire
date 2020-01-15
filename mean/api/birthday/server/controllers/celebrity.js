const mongoose = require('mongoose');
const Celeb = require('../models/celebrity');

module.exports = {
    index: (req,res) => {
        Celeb.find()
            .then(data => res.json(data))
            .catch(err => res.json(err))
    },
    create: (req,res) => {
        Celeb.create(req.body)
            .then(data => res.json(data))
            .catch(err => res.json(err))
    },
    delete: (req,res) => {
        Celeb.deleteOne({name: req.params.name})
            .then(data => res.json(data))
            .catch(err => res.json(err))
    },
    show: (req,res) => {
        Celeb.findOne({name: req.params.name})
            .then(data => res.json(data))
            .catch(err => res.json(err))
    }
};