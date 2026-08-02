const fs = require("fs");
const path = require("path");
const os = require("os");

const getHostname = () => {
  return os.hostname();
}
const getColor = () => {
  let color = process.env.DEFAULT_COLOR;
  const filePath = process.env.COLOR_CONFIG_PATH;

  if (filePath) {
    console.log("Color Config Path Found !");
    
    try {
      const colorFromFile = fs.readFileSync(
        path.resolve(filePath),
        "utf8"
      );
      console.log("color was changed");
      
      color = colorFromFile.trim();
    } catch (error) {
      console.error(`Failed to read contents of ${filePath}`);
      console.error(error);
    }
  }

  return color || "blue";
};

module.exports = {
  getColor,
  getHostname,
};