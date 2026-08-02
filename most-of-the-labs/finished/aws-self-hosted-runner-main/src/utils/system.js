'use strict';

const os = require('node:os');
const process = require('node:process');

/**
 * Returns key information about the host machine.
 * @returns {{ hostname: string, platform: string, arch: string, uptimeSeconds: number, nodeVersion: string, cpus: number, memoryMB: number }}
 */
function getMachineInfo() {
  return {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    uptimeSeconds: Math.floor(os.uptime()),
    nodeVersion: process.version,
    cpus: os.cpus().length,
    memoryMB: Math.round(os.totalmem() / 1024 / 1024),
  };
}

module.exports = { getMachineInfo };
