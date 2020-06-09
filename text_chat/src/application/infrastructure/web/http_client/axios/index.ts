import axios from 'axios';
import Failure from '../../../../../domain/entity/failure';
import { Either, left, right } from '../../../../../domain/types';
import HttpResponse from '../../entity/http_response';
import HttpClientInterface from '../index';

export default class AxiosHttpClient implements HttpClientInterface {
  public get({ endpoint, config }: { endpoint: string; config?: any }): Promise<Either<Failure, HttpResponse>> {
    return axios
      .get(endpoint, config)
      .then((response) => right(new HttpResponse({ data: response.data, statusCode: response.status })))
      .catch((error) => left(new Failure({ error })));
  }

  public post({
    endpoint,
    data,
    config,
  }: {
    endpoint: string;
    data: any;
    config?: any;
  }): Promise<Either<Failure, HttpResponse>> {
    return axios
      .post(endpoint, data, config)
      .then((response) => right(new HttpResponse({ data: response.data, statusCode: response.status })))
      .catch((error) => left(new Failure({ error })));
  }
}
