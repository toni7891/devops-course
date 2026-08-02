const rootRouter = require("express").Router();


rootRouter.get("/", (req, res) => {
  res.send(
    `<h1 style="color:${getColor()};">Hello from Color API</h1> 
    <h2>Hostname: ${getHostname()}</h2>`,
  );
});

module.exports = rootRouter;