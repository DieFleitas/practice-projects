const ExpressServer = require("./server/expressServer.js");
const config = require("../config");
const logger = require("./logger");

module.exports = async () => {
  const server = new ExpressServer();
  logger.info("> Express server loaded");

  server.start();
  logger.info(`> Server running on port: ${config.port}`);
};
