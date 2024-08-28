const dotenv = require("dotenv");

const envFound = dotenv.config();
if (!envFound) {
  throw new Error("Could not find .env file");
}

process.env.NODE_ENV = process.env.NODE_ENV || "development";

module.exports = {
  port: process.env.PORT,
  api: {
    prefix: "/api/v1",
  },
  log: {
    level: process.env.LOG_LEVEL,
  },
  swagger: {
    path: "/docs",
  },
  mapbox: {
    pathBase: "https://api.mapbox.com/geocoding/v5/mapbox.places",
    apiKey: process.env.MAPBOX_API_KEY,
  },
  openWeatherMap: {
    pathBase: "https://api.openweathermap.org/data/2.5/weather",
    apiKey: process.env.OPENWEATHERMAP_API_KEY,
  },
};
