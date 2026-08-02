import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';

describe('AppModule (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterEach(async () => {
    await app.close();
  });

  it('/health (GET)', () => {
    return request(app.getHttpServer())
      .get('/health')
      .expect(200)
      .expect((res) => {
        if (res.body.status !== 'ok') throw new Error('status not ok');
      });
  });

  it('/version (GET)', () => {
    return request(app.getHttpServer())
      .get('/version')
      .expect(200)
      .expect((res) => {
        for (const k of ['version', 'commit', 'buildDate']) {
          if (!(k in res.body)) throw new Error(`missing ${k}`);
        }
      });
  });
});
