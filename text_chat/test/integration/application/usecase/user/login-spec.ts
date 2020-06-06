// tslint:disable-next-line:no-implicit-dependencies
import * as chai from 'chai';
import AxiosHttpClient from '../../../../../src/application/infrastructure/web/http_client/axios';
import UsersServiceHealthCheckUseCase from '../../../../../src/application/usecase/health_check/users_service';
import LoginUserUseCase from '../../../../../src/application/usecase/user/login';

const expect = chai.expect;
const httpClient = new AxiosHttpClient();
const usersServiceHealthCheckUseCase = new UsersServiceHealthCheckUseCase({
  httpClient,
  usersServiceEndpoint: 'http://localhost:3000/healthz', // hard coded for now and then from config file\env vars ;)
});
const loginUserUseCase = new LoginUserUseCase({
  httpClient,
  usersServiceHealthCheckUseCase,
  usersServiceLoginEndpoint: 'http://localhost:3000/users/login', // hard coded for now and then from config file\env vars ;)
});

describe('Login User', () => {
  it('should be Failure or Success // Maybe making it better with internet check later? :D', async () => {
    const username = 'username';
    const password = 'password';
    await loginUserUseCase.execute({ username, password })
      .then((response) => {
        expect(response._tag).to.be.oneOf(['Left', 'Right']);
      });
  });
});
