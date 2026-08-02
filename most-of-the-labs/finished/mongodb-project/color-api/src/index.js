const express = require("express")
const mongoose = require("mongoose")
const bodyParser = require("body-parser")

const healthRouter = require("./routes/health")
const apiRouter = require("./routes/api")
const rootRouter = require("./routes/root")

const port = 80
const app = express()

const delayStartup = process.env.DELAY_STARTUP === "true"
console.log(`Delay startup: ${delayStartup}`)

app.use(bodyParser.json())
app.use("/", healthRouter)
app.use("/api", apiRouter)
app.use("/", rootRouter)

if (delayStartup) {
  const start = Date.now()
  while (Date.now() - start < 60000) {}
}

mongoose
  .connect(process.env.DB_URL)
  .then(() => {
    console.log("Connected to MongoDB")

    app.listen(port, () => {
      console.log(`Color API listening on port: ${port}`)
    })
  })
  .catch((error) => {
    console.error("Could not connect to MongoDB")
    console.error(error)
  })
