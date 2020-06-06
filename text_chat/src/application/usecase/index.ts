// tslint:disable-next-line:interface-name
import Failure from '../../domain/entity/failure';
import { Either } from '../../domain/types';

// tslint:disable-next-line:interface-name
export default interface UseCaseInterface {
  execute({ ...args }): Promise<Either<Failure, any>>;
}
