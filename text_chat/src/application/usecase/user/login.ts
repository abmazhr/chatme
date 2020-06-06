import AccessToken from '../../../domain/entity/access_token';
import Failure from '../../../domain/entity/failure';
import { Either, right } from '../../../domain/types';
import HttpClientInterface from '../../infrastructure/web/http_client';
import UsersServiceHealthCheckUseCase from '../health_check/users_service';
import UseCaseInterface from '../index';

export default class LoginUserUseCase implements UseCaseInterface {
  // tslint:disable-next-line:variable-name
  private readonly _usersServiceUseCase: UsersServiceHealthCheckUseCase;
  // tslint:disable-next-line:variable-name
  private readonly _httpClient: HttpClientInterface;
  // tslint:disable-next-line:variable-name
  private readonly _usersServiceLoginEndpoint: string;

  constructor({ usersServiceHealthCheckUseCase, httpClient, usersServiceLoginEndpoint }: {
    usersServiceHealthCheckUseCase: UsersServiceHealthCheckUseCase,
    httpClient: HttpClientInterface,
    usersServiceLoginEndpoint: string
  }) {
    this._usersServiceUseCase = usersServiceHealthCheckUseCase;
    this._httpClient = httpClient;
    this._usersServiceLoginEndpoint = usersServiceLoginEndpoint;
  }

  public execute({ username, password }: {
    username: string,
    password: string
  }): Promise<Either<Failure, AccessToken>> {
    return Promise.resolve(this._usersServiceUseCase.execute()
      .then((healthCheckResponse) => {
        switch (healthCheckResponse._tag) {
          case 'Left':
            return healthCheckResponse;
          case 'Right':
            return this._httpClient.post({ endpoint: this._usersServiceLoginEndpoint, data: { username, password } })
              .then((LoginResponse) => {
                switch (LoginResponse._tag) {
                  case 'Left':
                    return LoginResponse;
                  case 'Right':
                    return right(LoginResponse.right.data as AccessToken);
                }
              });
        }
      }));
  }
}
