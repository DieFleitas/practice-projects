const express = require("express");
const Success = require("../handlers/successHandler.js");
const { findCities } = require("../services/cityService.js");

/**
 *
 * @param {express.Request} req
 * @param {express.Response} res
 */
const cities = async (req, res, next) => {
  try {
    const cities = await findCities(req.params.city);
    const success = new Success(cities);
    res.json(success);
  } catch (error) {
    next(error);
  }
};

module.exports = {
  cities,
};
