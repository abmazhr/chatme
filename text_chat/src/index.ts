import SocketRegistryContainer from './application/infrastructure/web/entity/sockets_registry';
import AxiosHttpClient from './application/infrastructure/web/http_client/axios';
import ExpressWebSockets from './application/infrastructure/web/sockets/express_sockets';
import UsersServiceHealthCheckUseCase from './application/usecase/health_check/users_service';
import LoginUserUseCase from './application/usecase/user/login';

const httpClient = new AxiosHttpClient();

new ExpressWebSockets({
  socketRegistryContainers: [
    new SocketRegistryContainer({
      eventHandler: ExpressWebSockets.login({
        loginUserUseCase: new LoginUserUseCase({
          httpClient,
          usersServiceHealthCheckUseCase: new UsersServiceHealthCheckUseCase({
            httpClient,
            usersServiceHealthCheckEndpoint: 'http://localhost:3000/healthz',
          }),
          usersServiceLoginEndpoint: 'http://localhost:3000/users/login',
        }),
      }),
      eventName: 'connection',
    }),
  ],
  // tslint:disable-next-line:no-console
}).serve({ port: 3001, starterFunc: () => console.log('Listening on port 3001') });
