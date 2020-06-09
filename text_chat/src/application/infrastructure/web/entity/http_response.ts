export default class HttpResponse {
  public readonly data: any;
  public readonly statusCode: number;

  constructor({ data, statusCode }: { data: any; statusCode: number }) {
    this.data = data;
    this.statusCode = statusCode;
  }
}
