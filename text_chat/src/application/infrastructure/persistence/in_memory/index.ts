import AccessToken from '../../../../domain/entity/access_token';
import Failure from '../../../../domain/entity/failure';
import Success from '../../../../domain/entity/success';
import { Either, left, right } from '../../../../domain/types';
import PersistenceInterface from '../index';

export default class InMemoryDatabase implements PersistenceInterface {
  // tslint:disable-next-line:variable-name
  private _db: { [usernames: string]: AccessToken } = {};

  public fetchAccessToken({ username }: { username: string }): Either<Failure, AccessToken> {
    const fetchStatus: AccessToken = this._db[username];
    return fetchStatus
      ? right(fetchStatus)
      : left(new Failure({ error: `There is no access-token for user ${username}` }));
  }

  public persistAccessToken({ username, accessToken }: {
    username: string;
    accessToken: AccessToken;
  }): Either<Failure, Success> {
    try {
      this._db[username] = accessToken;
      return right(new Success());
    } catch (e) {
      return left(new Failure(e.toString()));
    }
  }
}
