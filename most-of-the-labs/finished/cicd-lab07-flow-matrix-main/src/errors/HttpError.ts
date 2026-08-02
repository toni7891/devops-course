export class HttpError extends Error {
  status: number;
  details?: unknown;

  constructor(status: number, message: string, details?: unknown) {
    super(message);
    this.status = status;
    this.details = details;
  }
  static notFound(msg = 'Not Found') { return new HttpError(404, msg); }
  static badRequest(msg = 'Bad Request', details?: unknown) { return new HttpError(400, msg, details); }
  static conflict(msg = 'Conflict') { return new HttpError(409, msg); }
}
