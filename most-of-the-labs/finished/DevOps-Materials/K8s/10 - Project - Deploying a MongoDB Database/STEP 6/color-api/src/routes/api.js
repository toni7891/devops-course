const express = require("express")

// Utils
const { getColor, getHostname} = require("../utils.js");

const hostname = getHostname();
const apiRouter = express.Router()
const color = getColor();

apiRouter.get("/", (req, res) => {
  const { format } = req.query; // localhost/api?format=text
  if (format === "json") {
    return res.json({
      color,
      hostname,
    });
  } else {
    return res.send(`COLOR: ${color}, HOSTNAME: ${hostname}`);
  }
}); 

module.exports = apiRouter