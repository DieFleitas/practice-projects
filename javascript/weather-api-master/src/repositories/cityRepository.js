const axios = require("axios");
const config = require("../config");

class CityRepository {
  constructor() {
    this.limit = 10;
    this.language = "es";
    this.pathBase = config.mapbox.pathBase;
    this.apiKey = config.mapbox.apiKey;
  }

  async findCities(city) {
    try {
      const instance = axios.create({
        baseURL: `${this.pathBase}/${city}.json`,
        params: {
          "access_token": this.apiKey,
          "limit": this.limit,
          "language": this.language,
        },
      });
      const response = await instance.get();

      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

module.exports = CityRepository;
