// tslint:disable-next-line:no-implicit-dependencies
import * as chai from 'chai';
import InMemoryDatabase from '../../../../../src/application/infrastructure/persistence/in_memory';
import FetchAccessTokenUseCase from '../../../../../src/application/usecase/access_token/fetch';
import PersistAccessTokenUseCase from '../../../../../src/application/usecase/access_token/persist';
import AccessToken from '../../../../../src/domain/entity/access_token';

const expect = chai.expect;
const persistence = new InMemoryDatabase();
const persistUseCase = new PersistAccessTokenUseCase(persistence);
const fetchUseCase = new FetchAccessTokenUseCase(persistence);

describe('Valid fetch of an access-token', () => {
  it('should return a Right', async () => {
    const username = 'test';
    const accessToken = new AccessToken({ token: 'valid_token_for_now' });
    await persistUseCase.execute({ username, accessToken })
      .then((response) => {
        expect(response._tag).to.eq('Right');
      });
    await fetchUseCase.execute({ username })
      .then((response) => {
        expect(response._tag).to.eq('Right');
      });
  });
});

describe('Invalid fetch of an access-token', () => {
  it('should return a Left', async () => {
    const username = 'not_persisted_username';
    await fetchUseCase.execute({ username })
      .then((response) => {
        expect(response._tag).to.eq('Left');
      });
  });
});
