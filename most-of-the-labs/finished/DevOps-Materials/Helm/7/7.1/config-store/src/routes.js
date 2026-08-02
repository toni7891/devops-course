const express = require("express");
const { KV } = require("./models");

const apiRouter = express.Router();

apiRouter.get("/kv", async (req, res) => {
  try {
    const kvs = await KV.findAll();
    return res.json({ data: kvs });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

apiRouter.get("/kv/:key", async (req, res) => {
  const { key } = req.params;
  try {
    const kv = await KV.findOne({ where: { key }});

    if (kv) {
      return res.json({ data: kv });
    } else {
      return res.status(404).json({ error: "Key not found" });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

apiRouter.post("/kv", async (req, res) => {
  try {
    const { key, value } = req.body;

    if (!key || !value) {
      return res.status(400).json({
        error: "Both key and value fields are required",
      });
    }

    const existingKV = await KV.findOne({
      where: { key },
    });

    if (existingKV) {
      return res.status(400).json({
        error: "Key already present in DB",
      });
    }

    const newKV = await KV.create({ key, value });

    return res.status(201).json({
      data: newKV,
    });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

apiRouter.put("/kv/:key", async (req, res) => {
  try {
    const { value } = req.body;
    const { key } = req.params;

    if (!value) {
      return res.status(400).json({
        error: "Value field is required",
      });
    }

    const [updatedCount] = await KV.update(
      { value },
      {
        where: { key },
      },
    );

    if (updatedCount > 0) {
      const updatedKV = await KV.findOne({
        where: { key },
      });

      if (updatedKV) {
        return res.json({
          data: updatedKV,
        });
      } else {
        return res.status(404).json({
          error: "Key not found",
        });
      }
    } else {
      return res.status(404).json({
        error: "Key not found",
      });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

apiRouter.delete("/kv/:key", async (req, res) => {
  try {
    const { key } = req.params;

    const deleted = await KV.destroy({
      where: { key },
    });

    if (deleted > 0) {
      return res.sendStatus(204);
    } else {
      return res.status(404).json({
        error: "Key not found",
      });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

module.exports = apiRouter;
