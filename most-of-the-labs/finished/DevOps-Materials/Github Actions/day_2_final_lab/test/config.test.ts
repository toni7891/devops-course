describe('config defaults', () => {
  const ORIGINAL_ENV = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...ORIGINAL_ENV };
  });

  afterAll(() => {
    process.env = ORIGINAL_ENV;
  });

  it('uses default values when env vars are absent', async () => {
    delete process.env.NODE_ENV;
    delete process.env.PORT;
    delete process.env.LOG_LEVEL;
    delete process.env.APP_VERSION;

    const { config } = await import('../src/config');
    expect(config.nodeEnv).toBe('development');
    expect(config.port).toBe(3000);
    expect(config.logLevel).toBe('info');
    expect(config.appVersion).toBe('1.0.0');
  });

  it('reads values from env vars', async () => {
    process.env.NODE_ENV = 'production';
    process.env.PORT = '8080';
    process.env.LOG_LEVEL = 'debug';
    process.env.APP_VERSION = '2.0.0';

    const { config } = await import('../src/config');
    expect(config.nodeEnv).toBe('production');
    expect(config.port).toBe(8080);
    expect(config.logLevel).toBe('debug');
    expect(config.appVersion).toBe('2.0.0');
  });
});

describe('errorHandler', () => {
  it('defaults statusCode to 500 when not set', async () => {
    const { errorHandler } = await import('../src/middleware/errorHandler');
    const err = new Error('boom');
    const jsonMock = jest.fn();
    const statusMock = jest.fn().mockReturnValue({ json: jsonMock });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const res = { status: statusMock } as any;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    errorHandler(err, {} as any, res, jest.fn() as any);

    expect(statusMock).toHaveBeenCalledWith(500);
    expect(jsonMock).toHaveBeenCalledWith({ success: false, error: 'Internal Server Error' });
  });

  it('uses provided statusCode and message', async () => {
    const { errorHandler } = await import('../src/middleware/errorHandler');
    const err = Object.assign(new Error('Not Found'), { statusCode: 404 });
    const jsonMock = jest.fn();
    const statusMock = jest.fn().mockReturnValue({ json: jsonMock });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const res = { status: statusMock } as any;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    errorHandler(err, {} as any, res, jest.fn() as any);

    expect(statusMock).toHaveBeenCalledWith(404);
    expect(jsonMock).toHaveBeenCalledWith({ success: false, error: 'Not Found' });
  });
});
