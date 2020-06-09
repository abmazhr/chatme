import * as chai from 'chai';
import AxiosHttpClient from '../../../../../src/application/infrastructure/web/http_client/axios';
import UsersServiceHealthCheckUseCase from '../../../../../src/application/usecase/health_check/users_service';

const expect = chai.expect;

describe('Users Service Health check natively', () => {
  const httpClient = new AxiosHttpClient();
  const usersServiceHealthCheckUseCase = new UsersServiceHealthCheckUseCase({
    httpClient,
    usersServiceHealthCheckEndpoint: 'http://localhost:3000/healthz', // hard coded for now and then from config file\env vars ;)
  });

  it('should be Failure or Success // Maybe making it better with internet check later? :D', async () => {
    await usersServiceHealthCheckUseCase.execute().then(response => {
      expect(response._tag).to.be.oneOf(['Right', 'Left']);
    });
  });
});
