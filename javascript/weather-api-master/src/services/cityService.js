const CityRepository = require("../repositories/cityRepository.js");
const repository = new CityRepository();

const findCities = async (city) => {
  const cities = await repository.findCities(city);

  return cities.features.map((element) => {
    return {
      id: element.id,
      name: element.name,
      log: element.geometry.coordinates[0],
      lat: element.geometry.coordinates[1],
    };
  });
};

module.exports = {
  findCities,
};
