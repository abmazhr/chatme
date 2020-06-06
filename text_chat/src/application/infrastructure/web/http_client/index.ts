// tslint:disable-next-line:interface-name
import Failure from '../../../../domain/entity/failure';
import { Either } from '../../../../domain/types';
import HttpResponse from '../entity/http_response';

// tslint:disable-next-line:interface-name
export default interface HttpClientInterface {
  get({ endpoint, config }: {
    endpoint: string,
    config?: any
  }): Promise<Either<Failure, HttpResponse>>

  post({ endpoint, data, config }: {
    endpoint: string,
    data: any,
    config?: any
  }): Promise<Either<Failure, HttpResponse>>
}
