const { Router } = require("express");
const router = Router();

const { weatherByCoordinates, weatherByCityId } = require("../controllers/weather");

router.get("/", weatherByCoordinates);
router.get("/:city/:id", weatherByCityId);


module.exports = router;
