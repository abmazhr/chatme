import AccessToken from '../../../domain/entity/access_token';
import Failure from '../../../domain/entity/failure';
import Success from '../../../domain/entity/success';
import { Either } from '../../../domain/types';
import PersistenceInterface from '../../infrastructure/persistence';
import UseCaseInterface from '../index';

export default class PersistAccessTokenUseCase implements UseCaseInterface {
  // tslint:disable-next-line:variable-name
  private _persistence: PersistenceInterface;

  constructor(persistence: PersistenceInterface) {
    this._persistence = persistence;
  }

  public execute({
    username,
    accessToken,
  }: {
    username: string;
    accessToken: AccessToken;
  }): Promise<Either<Failure, Success>> {
    return Promise.resolve(this._persistence.persistAccessToken({ username, accessToken }));
  }
}
