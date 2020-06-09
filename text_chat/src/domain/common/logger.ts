import dotenv from 'dotenv';
import pino from 'pino';

dotenv.config();

const logger = pino({
  name: process.env.APP_ID,
  level: process.env.LOG_LEVEL,
});

export default logger;
