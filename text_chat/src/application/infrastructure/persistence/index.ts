import AccessToken from '../../../domain/entity/access_token';
import Failure from '../../../domain/entity/failure';
import Success from '../../../domain/entity/success';
import { Either } from '../../../domain/types';

// tslint:disable-next-line:interface-name
export default interface PersistenceInterface {
  persistAccessToken({
    username,
    accessToken,
  }: {
    username: string;
    accessToken: AccessToken;
  }): Either<Failure, Success>;

  fetchAccessToken({ username }: { username: string }): Either<Failure, AccessToken>;
}
