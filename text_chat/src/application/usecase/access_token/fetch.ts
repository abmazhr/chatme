import AccessToken from '../../../domain/entity/access_token';
import Failure from '../../../domain/entity/failure';
import { Either } from '../../../domain/types';
import PersistenceInterface from '../../infrastructure/persistence';
import UseCaseInterface from '../index';

export default class FetchAccessTokenUseCase implements UseCaseInterface {
  // tslint:disable-next-line:variable-name
  private _persistence: PersistenceInterface;

  constructor(persistence: PersistenceInterface) {
    this._persistence = persistence;
  }

  public execute({ username }: { username: string }): Promise<Either<Failure, AccessToken>> {
    return Promise.resolve(this._persistence.fetchAccessToken({ username }));
  }
}
