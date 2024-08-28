const express = require("express");

/**
 *
 * @param {express.Request} req
 * @param {express.Response} res
 */
const getAllUsers = (req, res) => {
  const users = [];
  res.json(users);
};

/**
 *
 * @param {express.Request} req
 * @param {express.Response} res
 */
const createUser = (req, res) => {
  const result = {
    message: "User created",
  };
  res.json(result);
};

/**
 *
 * @param {express.Request} req
 * @param {express.Response} res
 */
const updateUser = (req, res) => {
  const { id } = req.params;
  const result = {
    message: "User updated",
  };
  res.json(result);
};

/**
 *
 * @param {express.Request} req
 * @param {express.Response} res
 */
const updatePartialUser = (req, res) => {
  const { id } = req.params;
  const result = {
    message: "User updated with patch",
  };
  res.json(result);
};

/**
 *
 * @param {express.Request} req
 * @param {express.Response} res
 */
const deleteUser = (req, res) => {
  const { id } = req.params;
  const result = {
    message: "User deleted",
  };
  res.json(result);
};

module.exports = {
  getAllUsers,
  createUser,
  updateUser,
  updatePartialUser,
  deleteUser,
};
