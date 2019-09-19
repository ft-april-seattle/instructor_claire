const mongoose = require('mongoose');

const SharkSchema = new mongoose.Schema({
    name: {type: String, required: [true, "A cute name is required."], minlength: [5, "The cute name must be at least 5 characters."], maxlength: [45, "The cute name must be no more than 45 characters."]},
    species: {type: String, required: [true, "A species is required."], minlength: [5, "The species must be at least 5 characters."], maxlength: [255, "The species must be no more than 45 characters."]},
    location: {type: String, required: [true, "A location is required."], minlength: [5, "The location must be at least 5 characters."], maxlength: [255, "The location must be no more than 45 characters."]},
    img: {type: String}
    },
    {timestamps: true}
);

module.exports = mongoose.model("Shark", SharkSchema);