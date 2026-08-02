const express = require("express")
const { getColor, getHostname } = require("../utils")

const rootRouter = express.Router()

rootRouter.get("/", (req, res) => {
  const color = getColor()
  const hostname = getHostname()

  res.json({
    color,
    hostname
  })
})

module.exports = rootRouter
