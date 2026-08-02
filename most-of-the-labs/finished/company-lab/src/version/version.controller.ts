import { Controller, Get } from '@nestjs/common';

@Controller('version')
export class VersionController {
  @Get()
  info() {
    return {
      version: process.env.APP_VERSION ?? 'dev',
      commit: process.env.COMMIT_SHA ?? 'unknown',
      buildDate: process.env.BUILD_DATE ?? 'unknown',
    };
  }
}
