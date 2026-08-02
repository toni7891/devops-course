"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.HealthController = void 0;
const common_1 = require("@nestjs/common");
const express_1 = require("express");
const pg_1 = require("pg");
const database_module_1 = require("../database/database.module");
let HealthController = class HealthController {
    constructor(pool) {
        this.pool = pool;
    }
    getHealth() {
        return { status: 'ok', timestamp: new Date().toISOString() };
    }
    async getReady(res) {
        try {
            await this.pool.query('SELECT 1');
            res.status(common_1.HttpStatus.OK).json({ status: 'ready' });
        }
        catch {
            res.status(common_1.HttpStatus.SERVICE_UNAVAILABLE).json({ status: 'not ready' });
        }
    }
};
exports.HealthController = HealthController;
__decorate([
    (0, common_1.Get)('health'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Object)
], HealthController.prototype, "getHealth", null);
__decorate([
    (0, common_1.Get)('ready'),
    __param(0, (0, common_1.Res)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [typeof (_a = typeof express_1.Response !== "undefined" && express_1.Response) === "function" ? _a : Object]),
    __metadata("design:returntype", Promise)
], HealthController.prototype, "getReady", null);
exports.HealthController = HealthController = __decorate([
    (0, common_1.Controller)(),
    __param(0, (0, common_1.Inject)(database_module_1.DATABASE_POOL)),
    __metadata("design:paramtypes", [pg_1.Pool])
], HealthController);
//# sourceMappingURL=health.controller.js.map