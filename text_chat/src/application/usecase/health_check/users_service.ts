import Failure from '../../../domain/entity/failure';
import Success from '../../../domain/entity/success';
import { Either, right } from '../../../domain/types';
import HttpClientInterface from '../../infrastructure/web/http_client';
import UseCaseInterface from '../index';


export default class UsersServiceHealthCheckUseCase implements UseCaseInterface {
  // tslint:disable-next-line:variable-name
  private readonly _usersServiceHealthCheckEndpoint: string;
  // tslint:disable-next-line:variable-name
  private readonly _httpClient: HttpClientInterface;

  constructor({ usersServiceEndpoint, httpClient }: {
    usersServiceEndpoint: string,
    httpClient: HttpClientInterface
  }) {
    this._usersServiceHealthCheckEndpoint = usersServiceEndpoint;
    this._httpClient = httpClient;
  }

  public execute(): Promise<Either<Failure, Success>> {
    return this._httpClient.get({ endpoint: this._usersServiceHealthCheckEndpoint })
      .then((response) => {
        switch (response._tag) {
          case 'Left':
            return response;
          case 'Right':
            return right(new Success());
        }
      });
  }
}
