const express = require("express")
const { getColor, getColors, saveColor, deleteColor } = require("../db/color")

const apiRouter = express.Router()

apiRouter.get("/", async (req, res) => {
  const colorKey = req.query.colorKey
  const color = await getColor(colorKey)

  res.send(`COLOR: ${color}`)
})

apiRouter.get("/color", async (req, res) => {
  const colors = await getColors()

  res.send(colors)
})

apiRouter.get("/color/:colorKey", async (req, res) => {
  const key = req.params.colorKey
  const color = await getColor(key, true)

  if (!color) {
    return res.sendStatus(404)
  }

  res.send(color)
})

apiRouter.post("/color/:colorKey", async (req, res) => {
  const key = req.params.colorKey
  const value = req.body.value

  await saveColor(key, value)

  res.status(201).send({ key, value })
})

apiRouter.delete("/color/:colorKey", async (req, res) => {
  const key = req.params.colorKey

  await deleteColor(key)

  res.sendStatus(204)
})

module.exports = apiRouter
