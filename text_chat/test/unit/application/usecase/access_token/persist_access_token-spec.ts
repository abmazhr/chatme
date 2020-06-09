// tslint:disable-next-line:no-implicit-dependencies
import * as chai from 'chai';
import InMemoryDatabase from '../../../../../src/application/infrastructure/persistence/in_memory';
import PersistAccessTokenUseCase from '../../../../../src/application/usecase/access_token/persist';

const expect = chai.expect;
const persistence = new InMemoryDatabase();
const persistUseCase = new PersistAccessTokenUseCase(persistence);

describe('Valid persist of an access-token', () => {
  it('should return a Right', async () => {
    const username = 'test';
    const accessToken = { token: 'valid_token_for_now' };
    await persistUseCase.execute({ username, accessToken }).then(response => {
      expect(response._tag).to.eq('Right');
    });
  });
});
