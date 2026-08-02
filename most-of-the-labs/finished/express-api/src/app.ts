import express from 'express';
import { errorHandler } from './middleware/errorHandler.js';
import router from './routes/index.js';
const app = express();
app.use(express.json());
app.use('/', router);
app.use(errorHandler);
export default app;
