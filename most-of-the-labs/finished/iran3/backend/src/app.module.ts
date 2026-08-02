import { Module } from '@nestjs/common';
import { DatabaseModule } from './database/database.module';
import { ProductsModule } from './products/products.module';
import { HealthController } from './health/health.controller';

@Module({
  imports: [DatabaseModule, ProductsModule],
  controllers: [HealthController],
})
export class AppModule {}
