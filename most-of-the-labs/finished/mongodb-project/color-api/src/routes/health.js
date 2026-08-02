const express = require("express")

const healthRouter = express.Router()

let failReadiness = false
let failLiveness = false

healthRouter.get("/ready", (req, res) => {
  if (failReadiness) {
    return res.status(500).send("NOT READY")
  }

  res.send("OK")
})

healthRouter.get("/health", (req, res) => {
  if (failLiveness) {
    return res.status(500).send("NOT HEALTHY")
  }

  res.send("OK")
})

healthRouter.get("/up", (req, res) => {
  res.send("OK")
})

module.exports = healthRouter
