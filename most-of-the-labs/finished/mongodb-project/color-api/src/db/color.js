const mongoose = require("mongoose")

const colorSchema = new mongoose.Schema({
  key: String,
  value: String
})

const Color = mongoose.model("Color", colorSchema)

const saveColor = async (key, value) => {
  let color = await Color.findOne({ key })

  if (color) {
    color.set({ value })
  } else {
    color = new Color({ key, value })
  }

  await color.save()
}

const getColor = async (key, strict) => {
  const color = await Color.findOne({ key })

  if (color) {
    return color.value
  }

  if (strict) {
    return null
  }

  return process.env.DEFAULT_COLOR || "blue"
}

const getColors = async () => {
  return Color.find()
}

const deleteColor = async (key) => {
  return Color.deleteOne({ key })
}

module.exports = {
  saveColor,
  getColor,
  getColors,
  deleteColor
}
