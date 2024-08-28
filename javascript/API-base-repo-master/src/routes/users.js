const { Router } = require("express");
const router = Router();

const {
  getAllUsers,
  createUser,
  updateUser,
  updatePartialUser,
  deleteUser,
} = require("../controllers/users");

router.get("/", getAllUsers);
router.post("/", createUser);
router.put("/:id", updateUser);
router.patch("/:id", updatePartialUser);
router.delete("/:id", deleteUser);

module.exports = router;