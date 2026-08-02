const fs = require("fs")
const path = require("path")
const os = require("os")

const getColor = () => {
  return process.env.DEFAULT_COLOR || "blue"
}

const getHostname = () => {
  return os.hostname()
}

module.exports = {
  getColor,
  getHostname
}
