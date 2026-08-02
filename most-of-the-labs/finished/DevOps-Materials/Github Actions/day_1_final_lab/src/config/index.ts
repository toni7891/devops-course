import dotenv from 'dotenv';

dotenv.config();

export interface AppConfig {
  nodeEnv: string;
  port: number;
  logLevel: string;
  appVersion: string;
}

export const config: AppConfig = {
  nodeEnv: process.env.NODE_ENV ?? 'development',
  port: parseInt(process.env.PORT ?? '3000', 10),
  logLevel: process.env.LOG_LEVEL ?? 'info',
  appVersion: process.env.APP_VERSION ?? '1.0.0',
};
