const axios = require("axios");
const config = require("../config");

class WeatherRepository {
  constructor() {
    this.units = "metric";
    this.lang = "es";
    this.pathBase = config.openWeatherMap.pathBase;
    this.apiKey = config.openWeatherMap.apiKey;
  }

  async weatherByCoordinates(lon, lat) {
    try {
      const instance = axios.create({
        baseURL: `${this.pathBase}/`,
        params: {
          access_token: this.apiKey,
          units: this.units,
          lang: this.lang,
          lon: lon,
          lat: lat,
        },
      });
      const response = await instance.get();

      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

module.exports = WeatherRepository;
