const express = require("express")
const { getColor } = require("../db/color")
const { getHostname } = require("../utils")

const rootRouter = express.Router()

rootRouter.get("/", async (req, res) => {
  const colorKey = req.query.colorKey
  const color = await getColor(colorKey)
  const hostname = getHostname()

  res.json({
    color,
    hostname
  })
})

module.exports = rootRouter
