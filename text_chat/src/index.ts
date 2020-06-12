import * as os from 'os';
import AxiosHttpClient from './application/infrastructure/web/http_client/axios';
import ExpressWebSockets from './application/infrastructure/web/sockets/express_sockets';
import UsersServiceHealthCheckUseCase from './application/usecase/health_check/users_service';
import LoginUserUseCase from './application/usecase/user/login';
import logger from './domain/common/logger';

const httpClient = new AxiosHttpClient();
const port = parseInt(process.env.PORT);
const usersServiceHealthCheckEndpoint = process.env.USERS_SERVICE_HEALTH_CHECK_ENDPOINT;
const usersServiceLoginEndpoint = process.env.USERS_SERVICE_LOGIN_ENDPOINT;

const loginUserUseCase = new LoginUserUseCase({
  httpClient,
  usersServiceHealthCheckUseCase: new UsersServiceHealthCheckUseCase({
    httpClient,
    usersServiceHealthCheckEndpoint,
  }),
  usersServiceLoginEndpoint,
});

new ExpressWebSockets({ loginUserUseCase }).serve({
  port,
  starterFunc: () => logger.info(
    `up and running in ${
      process.env.NODE_ENV || 'development'
    } @: ${os.hostname()} on port: ${port}`,
  ),
});
