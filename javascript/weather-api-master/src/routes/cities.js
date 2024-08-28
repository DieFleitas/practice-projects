const { Router } = require("express");
const router = Router();

const { cities } = require("../controllers/cities.js");

router.get("/:city", cities);

module.exports = router;
