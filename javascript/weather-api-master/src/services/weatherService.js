const CityRepository = require("../repositories/cityRepository.js");
const cityRepository = new CityRepository();
const WeatherRepository = require("../repositories/weatherRepository.js");
const weatherRepository = new WeatherRepository();

const weatherByCoordinates = async (lon, lat) => {
  try {
    const weather = await weatherRepository.weatherByCoordinates(lon, lat);

    return {
      description: weather.weather[0].description,
      temperature: weather.main.temp,
      temperatureMin: weather.main.temp_min,
      temperatureMax: weather.main.temp_max,
    };
  } catch (error) {
    throw error;
  }
};

const weatherByCityId = async (city, id) => {
  try {
    const cities = await cityRepository.findCities(city);

    const cityData = cities.features.find((element) => {
      return element.id === id;
    });

    const lon = cityData.geometry.coordinates[0];
    const lat = cityData.geometry.coordinates[1];

    return await weatherByCoordinates(lon, lat);
  } catch (error) {
    throw error;
  }
};

module.exports = {
  weatherByCoordinates,
  weatherByCityId,
};
